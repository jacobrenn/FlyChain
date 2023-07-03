from .feedback_handlers import submit_feedback, save_to_downloads, delete_csv, binary_feedback_handler, correction_feedback_handler
import gradio as gr    

def create_ui_with_feedback(respond, theme):
    with gr.Blocks(theme = theme) as ChatUI:
        chatbot = gr.Chatbot(value = [], elem_id = 'chatbot')
        with gr.Row():
            with gr.Column(scale = 100):
                msg = gr.Textbox(
                    show_label = False,
                    placeholder = 'Enter Text and Press Enter',
                    elem_id = 'user_msg_input'
                )

        with gr.Row():
            with gr.Column():
                binary = gr.Radio(['Good Response', 'Bad Response'],
                label = 'Was this a good response?', 
                value = None,
                elem_id = 'binary_feedback_selector')

        with gr.Row():
            with gr.Column(scale = 100):
                correction = gr.Textbox(
                    show_label = True,
                    label = 'Correction (optional)',
                    placeholder = 'Enter your correction here',
                    elem_id = 'user_correction_input'
                )

        with gr.Row():
            with gr.Column(scale = 100):
                submit_button = gr.Button(value = 'Submit Feedback', elem_id = 'submit_feedback_button')
        with gr.Row():
            with gr.Column(scale = 3):
                download_button = gr.Button(value = 'Download Feedback', elem_id = 'download_feedback_button')
            with gr.Column(scale = 1):
                delete_button = gr.Button(value = 'Clear Feedback', elem_id = 'clear_feedback_button')
        
        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        binary.change(fn = lambda choice: binary_feedback_handler(choice))
        correction.change(fn = lambda correction: correction_feedback_handler(correction), inputs = [correction])
        submit_button.click(fn = submit_feedback)
        download_button.click(fn = save_to_downloads)
        delete_button.click(fn = delete_csv)

        return ChatUI

def create_ui_without_feedback(respond, theme):
    with gr.Blocks(theme = theme) as ChatUI:
        chatbot = gr.Chatbot(value = [], elem_id = 'chatbot')
        with gr.Row():
            with gr.Column(scale = 100):
                msg = gr.Textbox(
                    show_label = False,
                    placeholder = 'Enter Text and Press Enter',
                    elem_id = 'user_msg_input'
                )
        msg.submit(respond, [msg, chatbot], [msg, chatbot])
    
    return ChatUI