import os
from nicegui import ui, app
from app.services import LMStudioService, DocumentProcessor
from config import config


def setup_ui():
    """Setup the NiceGUI interface"""
    
    # Initialize services
    llm_service = LMStudioService()
    
    # Check LM Studio connection
    llm_connected = llm_service.health_check()
    
    # Dark theme with custom styling
    ui.dark_mode()
    
    # Custom CSS for better styling
    ui.add_body_html('''
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0f0f0f;
        }
        .nicegui-card {
            background: #1e1e1e !important;
            border: 1px solid #333 !important;
        }
        textarea {
            background: #2d2d2d !important;
            color: #e0e0e0 !important;
            border: 1px solid #444 !important;
            overflow-y: scroll !important;
            resize: none !important;
        }
        textarea::-webkit-scrollbar {
            width: 12px;
        }
        textarea::-webkit-scrollbar-track {
            background: #1a1a1a;
        }
        textarea::-webkit-scrollbar-thumb {
            background: #555;
            border-radius: 6px;
        }
        textarea::-webkit-scrollbar-thumb:hover {
            background: #777;
        }
        textarea:focus {
            border-color: #1976d2 !important;
            box-shadow: 0 0 5px rgba(25, 118, 210, 0.3) !important;
        }
        button {
            transition: all 0.3s ease !important;
        }
        button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        }
        #results-area {
            height: calc(100vh - 250px) !important;
            min-height: 500px !important;
            max-height: none !important;
        }
    </style>
    ''')
    
    # Header
    with ui.header().classes('w-full bg-gradient-to-r from-blue-900 to-blue-700 shadow-lg'):
        with ui.row().classes('w-full items-center justify-between px-6 py-4'):
            ui.label('📊 Local LLM Document Analysis').classes('text-3xl font-bold text-white')
            
            # Connection indicator
            with ui.row().classes('items-center gap-2'):
                if llm_connected:
                    ui.icon('check_circle').classes('text-green-400 text-2xl')
                    ui.label('LM Studio Connected').classes('text-green-300 font-semibold')
                else:
                    ui.icon('error').classes('text-red-400 text-2xl')
                    ui.label('LM Studio Offline').classes('text-red-300 font-semibold')
    
    # Store current document
    current_state = {'text': None, 'name': None}
    
    # Main container with better layout
    with ui.column().classes('w-full h-screen bg-gray-900 overflow-hidden'):
        with ui.row().classes('w-full flex-1 gap-4 p-4 overflow-hidden'):
            
            # Left panel - Document Upload & Processing
            with ui.card().classes('w-1/3 bg-gray-800 shadow-xl rounded-lg overflow-y-auto'):
                ui.label('📤 Upload & Analyze').classes('text-2xl font-bold text-blue-400 mb-4')
                
                # File upload
                def on_upload_handler(e):
                    handle_file_upload(e, llm_service, current_state, doc_name_label, doc_size_label, doc_chars_label, result_output, query_input, loading_spinner)
                
                upload_files = ui.upload(
                    on_upload=on_upload_handler,
                    auto_upload=True,
                    max_file_size=config.MAX_UPLOAD_SIZE_BYTES
                ).classes('w-full')
                upload_files.tooltip = f"Max size: {config.MAX_UPLOAD_SIZE_MB}MB"
                
                ui.label(f"📎 Supported: {', '.join(config.SUPPORTED_FORMATS).upper()}").classes('text-sm text-gray-400 mt-2')
                
                ui.separator().classes('my-4')
                
                # Analysis query input
                ui.label('❓ Ask a Question:').classes('text-lg font-semibold text-white mt-4 mb-2')
                query_input = ui.textarea(
                    placeholder='What would you like to know about this document? Ask anything...',
                    value=''
                ).classes('w-full h-32 text-base')
                
                # Loading indicator
                loading_spinner = ui.spinner().classes('mt-4')
                loading_spinner.set_visibility(False)
                
                def analyze_current():
                    if not current_state['text']:
                        ui.notify('Please upload a document first', type='negative')
                        return
                    
                    query = query_input.value
                    if not query.strip():
                        ui.notify('Please enter a question', type='warning')
                        return
                    
                    loading_spinner.set_visibility(True)
                    result = llm_service.analyze_document(current_state['text'], query)
                    result_output.value = result or 'Error analyzing document'
                    loading_spinner.set_visibility(False)
                    ui.update(result_output)
                
                ui.button('🔍 Analyze', on_click=analyze_current).classes('w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 mt-4 rounded-lg')
            
            # Middle panel - Quick Actions & Document Info
            with ui.card().classes('w-1/3 bg-gray-800 shadow-xl rounded-lg overflow-y-auto'):
                ui.label('⚡ Quick Analysis').classes('text-2xl font-bold text-green-400 mb-4')
                
                def quick_summarize():
                    if not current_state['text']:
                        ui.notify('Please upload a document first', type='negative')
                        return
                    
                    loading_spinner.set_visibility(True)
                    result = llm_service.summarize(current_state['text'])
                    result_output.value = result or 'Error summarizing document'
                    query_input.value = '(Auto: Summary)'
                    loading_spinner.set_visibility(False)
                    ui.update(result_output)
                
                def quick_key_points():
                    if not current_state['text']:
                        ui.notify('Please upload a document first', type='negative')
                        return
                    
                    loading_spinner.set_visibility(True)
                    result = llm_service.extract_key_points(current_state['text'])
                    result_output.value = result or 'Error extracting key points'
                    query_input.value = '(Auto: Key Points)'
                    loading_spinner.set_visibility(False)
                    ui.update(result_output)
                
                ui.button('📝 Summarize', on_click=quick_summarize).classes('w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 rounded-lg mb-2')
                ui.button('🎯 Key Points', on_click=quick_key_points).classes('w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 rounded-lg')
                
                ui.separator().classes('my-6')
                
                # Document info
                ui.label('📄 Document Information').classes('text-lg font-semibold text-white mb-3')
                
                doc_info_section = ui.column().classes('bg-gray-700 p-4 rounded-lg')
                with doc_info_section:
                    doc_name_label = ui.label('No document loaded').classes('text-base text-gray-300 font-semibold')
                    doc_size_label = ui.label('').classes('text-sm text-gray-400 mt-1')
                    doc_chars_label = ui.label('').classes('text-sm text-gray-400 mt-1')
            
            # Right panel - Results
            with ui.card().classes('w-1/3 bg-gray-800 shadow-xl rounded-lg flex flex-col h-[calc(100vh-120px)]'):
                # Header
                ui.label('📋 Analysis Results').classes('text-2xl font-bold text-amber-400 px-4 pt-4 pb-2')
                
                ui.separator().classes('my-0')
                
                # Results textarea - takes all available space with scroll
                with ui.column().classes('flex-1 w-full px-4 py-4 overflow-hidden'):
                    result_output = ui.textarea(
                        placeholder='Analysis results will appear here automatically...\n\nLong text will scroll.\n\nUpload a document and click Analyze or use Quick Actions.',
                        value=''
                    ).props('id=results-area outlined readonly rows=25')
                    result_output.classes('w-full h-full text-base overflow-y-auto')
                    result_output.style('height: calc(100vh - 250px) !important; min-height: 500px; overflow-y: auto !important;')
                
                ui.separator().classes('my-0')
                
                # Action buttons at bottom
                with ui.row().classes('w-full gap-2 px-4 py-4'):
                    def copy_results():
                        if result_output.value:
                            ui.run_javascript(f'''
                                navigator.clipboard.writeText(`{result_output.value}`);
                            ''')
                            ui.notify('✅ Results copied!', type='positive')
                        else:
                            ui.notify('No results to copy', type='warning')
                    
                    def clear_results():
                        result_output.value = ''
                        query_input.value = ''
                        ui.update(result_output)
                        ui.notify('🗑️ Cleared', type='info')
                    
                    ui.button('📋 Copy', on_click=copy_results).classes('flex-1 bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded')
                    ui.button('🗑️ Clear', on_click=clear_results).classes('flex-1 bg-red-600 hover:bg-red-700 text-white font-bold py-3 rounded')


def handle_file_upload(e, llm_service, current_state, doc_name_label, doc_size_label, doc_chars_label, result_output, query_input, loading_spinner):
    """Handle file upload"""
    try:
        # Get uploaded file
        file_data = e.content.read()
        file_name = e.name
        
        # Create file path
        file_path = os.path.join(config.UPLOADS_DIR, file_name)
        
        # Validate file
        is_valid, message = DocumentProcessor.validate_file(file_path, len(file_data))
        if not is_valid:
            ui.notify(message, type='negative')
            return
        
        # Save file
        with open(file_path, 'wb') as f:
            f.write(file_data)
        
        # Process file
        text = DocumentProcessor.process_file(file_path)
        if not text:
            ui.notify('Error processing file', type='negative')
            return
        
        # Store text
        current_state['text'] = text
        current_state['name'] = file_name
        
        # Update UI
        doc_name_label.set_text(f'📄 {file_name}')
        doc_size_label.set_text(f'Size: {len(file_data) / 1024:.1f} KB')
        doc_chars_label.set_text(f'Characters: {len(text):,}')
        
        ui.notify(f'✅ Document loaded: {file_name}', type='positive')
        
    except Exception as e:
        ui.notify(f'Upload error: {str(e)}', type='negative')
