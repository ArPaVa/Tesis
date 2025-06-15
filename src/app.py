import streamlit as st
import time
import json
from settings import *
from main import audio_adjustments, parse_chunk, simple_transcription, summarize, create_audacity_project_edited, audiowork

st.set_page_config(layout="wide")
   
# Session settings
if 'summaries' not in st.session_state:
    st.session_state.summaries = []
if 'selected_segments' not in st.session_state:
    st.session_state.selected_segments = []
if 'source_transcription' not in st.session_state:
    st.session_state.source_transcription = []
if 'current_start' not in st.session_state:
    st.session_state.current_start = None
if 'current_end' not in st.session_state:
    st.session_state.current_end = None

# CSS style
st.markdown("""
<style>
    .scrollable-section {
        max-height: 600px;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #eee;
        border-radius: 5px;
        margin: 10px 0;
    }
    .segment-card {
        padding: 10px;
        margin: 5px 0;
        border-left: 4px solid #4CAF50;
        background-color: #f8f9fa;
    }
    .highlighted {
        background-color: #fff3cd !important;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("Configuración")

# Sidebar for settings
model_size = st.sidebar.selectbox(
    "Tamaño del modelo Whisper",
    ["tiny", "base", "small", "medium"],
    index=2
)    

@st.dialog("Crear Proyecto de Audacity")
def create_audacity_project():
    st.info('NOTE: Audacity must be running to use this function.')
    st.info("NOTE: If you have multiple Audacity windows open, the code work on the last Audacity window opened. You can't select which window you want the macros sent to.")
    if st.session_state.selected_segments:
        segments_tuples = []
        audio_duration = audiowork.get_audio_duration(st.session_state.file_path)/1000
        print(audio_duration)
        for idx, segment in enumerate(st.session_state.selected_segments):
            st.markdown(f"{idx+1}. `{segment['start']:.1f} - {segment['end']:.1f}`: {segment['text']}")
            segments_tuples.append((max(0,segment['start']-3), min(segment['end']+3, audio_duration))) # TODO fix max
        audacity_project_path = st.text_input("Path dónde crear el proyecto de audacity incluyendo extensión") # TODO create a function to read from default config
        if st.button("Crear"):
            print(segments_tuples)
            create_audacity_project_edited(st.session_state.file_path, segments_tuples, audacity_project_path)
            st.rerun()

tab1, tab2 = st.tabs(["Selección de Audio", "Selección de Segmentos"])

with tab1:
    st.title("Editor de Audio Inteligente")

    description = st.text_area("Descripción del contexto del audio")
    language = st.text_input("Idioma del audio", "es")

    # https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader
    uploaded_file = st.file_uploader("Sube tu archivo de audio", type=["wav", "mp3", "ogg"])
    # TODO By default, uploaded files are limited to 200 MB each. You can configure this using the server.maxUploadSize config option. 
    # For more information on how to set config options, see [config.toml](https://docs.streamlit.io/develop/api-reference/configuration/config.toml).

    if uploaded_file is not None and ('summaries' not in st.session_state or not st.session_state.summaries):
        with open(os.path.join(IN_PROCESS_DIR, f's_{uploaded_file.name}'), "wb") as file:
            file.write(uploaded_file.getvalue())

        with st.status("Procesando audio...", expanded=True) as status:
            st.write("Ajustando formato del audio...")
            start_time1 = time.time()

            file_path = audio_adjustments(os.path.join(IN_PROCESS_DIR, f's_{uploaded_file.name}'))
            st.session_state.file_path = file_path
            # st.session_state.file_path = '/home/niley/Documents/VSCode/Tesis/in_process/ready_mtest.wav'
            os.remove(os.path.join(IN_PROCESS_DIR, f's_{uploaded_file.name}'))
            st.write(f"Ajuste completado en {time.time()-start_time1:.1f}s")
            st.write("Transcribiendo audio...")
            start_time = time.time()

            simple_transcription(file_path, language, model_size)        
            st.write(f"Transcripción completada en {time.time()-start_time:.1f}s")
            st.write("Generando resúmenes...")
            start_time = time.time()

            output_json = summarize(description, file_path) 
            # output_json = os.path.join(FINISHED_DIR, f"summary_result_{os.path.splitext(os.path.basename(file_path))[0]}.json")
            with open(output_json, 'r') as file:
                st.session_state.summaries = json.load(file)
            st.write(f"Resumen completado en {time.time()-start_time:.1f}s")
            status.update(label=f"Proceso completado! {time.time()-start_time1:.1f}s", state="complete", expanded=True)
    
with tab2:
    st.title("Editor de Audio Inteligente")

    if 'summaries' not in st.session_state or not st.session_state.summaries:
        st.warning("Por favor procesa un audio en la pestaña 'Selección de Audio' primero")
        st.stop()

    # Main summary section
    col1, col2, col3 = st.columns([0.4, 0.4, 0.2])

    with col3:
        st.subheader("Segmento seleccionado:")        
        col3_1, col3_2 = st.columns(2)
        with col3_1:
            st.write("Inicio:")
            if st.session_state.current_start:
                st.write(f"**Tiempo:** {st.session_state.current_start['time']:.1f}s")
                # st.write(f"**Texto:** {st.session_state.current_start['text']}")
                st.write(f"**Fuente:** {st.session_state.current_start['source']}")
            else:
                st.write("No seleccionado")
                
        with col3_2:
            st.write("Fin:")
            if st.session_state.current_end:
                st.write(f"**Tiempo:** {st.session_state.current_end['time']:.1f}s")
                # st.write(f"**Texto:** {st.session_state.current_end['text']}")
                st.write(f"**Fuente:** {st.session_state.current_end['source']}")
            else:
                st.write("No seleccionado")
        if st.button("💾 Guardar Segmento") and st.session_state.current_start and st.session_state.current_end:
            if st.session_state.current_start['time'] < st.session_state.current_end['time']:
                new_segment = {
                    "start": st.session_state.current_start['time'],
                    "end": st.session_state.current_end['time'],
                    "text": f"{st.session_state.current_start['text']} [...] {st.session_state.current_end['text']}"
                }
                st.session_state.selected_segments.append(new_segment)
                st.success("Segmento guardado exitosamente!")
                del st.session_state.current_start
                del st.session_state.current_end
                st.rerun()
            else:
                st.error("El tiempo de inicio debe ser menor que el tiempo final")
            st.rerun()
        st.subheader("Segmentos Guardados")
        if not st.session_state.selected_segments:
            st.info("No hay segmentos guardados aún")
        else:
            for idx, segment in enumerate(st.session_state.selected_segments):
                with st.container():
                    st.markdown(f"**Segmento {idx+1}:** `{segment['start']:.1f}s - {segment['end']:.1f}s`")
                    st.caption(f"Text: {segment['text']}")
                    
                    # Delete button
                    if st.button(f"Eliminar Segmento {idx+1}", key=f"del_{idx}"):
                        st.session_state.selected_segments.remove(st.session_state.selected_segments[idx])
            if st.button(f"Crear Proyecto de Audacity"):
                create_audacity_project()
                        

    # Left Column: summaries
    with col1:

        # Section 1: Summary selection
        st.subheader("Resúmenes")
        summary_options = [f"Resumen {i+1}. [{s['start_time']:.1f}-{s['end_time']:.1f}s]" for i, s in enumerate(st.session_state.summaries)]

        selected_idx = st.selectbox("Selecciona un resumen:", range(len(summary_options)), format_func=lambda x: summary_options[x])

        st.session_state.selected_summary = st.session_state.summaries[selected_idx]
        st.subheader(f"Resumen seleccionado: {st.session_state.selected_summary['start_time']:.1f}s - {st.session_state.selected_summary['end_time']:.1f}s")
        with st.container(height=500):
            st.markdown(st.session_state.selected_summary['summary'])
        
    with col2:
        if st.session_state.selected_summary:  
            st.subheader(f"Transcripción del Audio del Resumen {selected_idx+1}")
            st.write("Selecciona segmentos de la transcripción:")
            
            with st.container(height=500):
                all_chunks = []
                for chunk_str in st.session_state.selected_summary['chunk']:
                    parsed = parse_chunk(chunk_str)
                    if parsed:
                        all_chunks.append(parsed)

                for i, chunk in enumerate(all_chunks):
                    st.write(f"**{chunk['start']:.1f}s-{chunk['end']:.1f}s:** {chunk['text']}")
                    col1, col2, col3 = st.columns([0.3, 0.3, 0.4])
                    with col1:
                        if st.button(f"Inicio_{i}", key=f"start_{selected_idx}_{i}"):
                            st.session_state.current_start = {
                                "time": chunk['start'],
                                "text": chunk['text'],
                                "source": f"Resumen {selected_idx+1}"
                            }
                            st.rerun()
                    with col2:
                        if st.button(f"Fin_{i}", key=f"end_{selected_idx}_{i}"):
                            st.session_state.current_end = {
                                "time": chunk['end'],
                                "text": chunk['text'],
                                "source": f"Resumen {selected_idx+1}"
                            }
                            st.rerun()
        
