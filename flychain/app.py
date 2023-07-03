from agent import create_agent
import gradio as gr
import shutil
import click
import csv
import os

@click.command()
@click.option('--model', '-m', default='gpt-4')
@click.option('--history/--no-history', default=True)
@click.option('--temperature', type=int, default=0)
@click.option('--task', type=str, default='text-generation')
@click.option('--huggingface-pipeline-kwargs', type=dict, default=None)
@click.option('--huggingface-model-kwargs', type=dict, default=None)
@click.option('--feedback', type=bool, default=True)

def deploy(model, history, temperature, task, huggingface_pipeline_kwargs, huggingface_model_kwargs, feedback):
    
    agent = create_agent(model='text-davinci-003', chat_history=history, temperature=temperature, task=task, huggingface_pipeline_kwargs=huggingface_pipeline_kwargs, huggingface_model_kwargs=huggingface_model_kwargs)

    chat = {'msg': None, 'bot_msg': None, 'binary_feedback' : None, 'correction' : None}

    def respond(msg, chat_history):
        bot_msg = agent.run(msg)
        chat_history.append((msg, bot_msg))
        chat['msg'] = msg
        chat['bot_msg'] = bot_msg
        return "", chat_history

    def binary_feedback_handler(choice):
        binary_feedback = 1 if choice == 'Upvote' else -1
        chat['binary_feedback'] = binary_feedback
    
    def correction_feedback_handler(correction):
        chat['correction'] = correction
   

    def submit_feedback():
        if chat['msg'] is not None and chat['bot_msg'] is not None:
           save_to_csv(chat['msg'], chat['bot_msg'], chat['binary_feedback'], chat['correction'])
           chat['msg'] = None
           chat['bot_msg'] = None
           chat['binary_feedback'] = None
           chat['correction'] = None

    
    def save_to_csv(msg, bot_msg, value, correction = None):
        csv_exists = os.path.isfile('./feedback.csv')
        with open('./feedback.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            if not csv_exists:
                writer.writerow(['user_prompt', 'bot_response', 'binary_feedback', 'correction'])
            writer.writerow([msg, bot_msg, value, correction])
    
    def save_to_downloads():
        filename = 'feedback.csv'
        home = os.path.expanduser("~")
        if os.name == 'nt':  # If the OS is Windows
            downloads_folder = os.path.join(home, 'Downloads')
        else:                # For UNIX, Linux, MacOS, etc.
            downloads_folder = os.path.join(home, 'Downloads')
            
        src_file = os.path.join(os.getcwd(), filename)
        dst_file = os.path.join(downloads_folder, filename)

        if not os.path.isfile(src_file):
            print(f"No such file {src_file} in the current directory.")
            return

        try:
            shutil.copy2(src_file, dst_file)
            print(f"File {filename} has been copied to {downloads_folder}")
        except PermissionError:
            print(f"Permission denied: could not copy {filename} to {downloads_folder}")
        except Exception as e:
            print(f"An error occurred while copying {filename} to {downloads_folder}: {e}")

    def delete_csv():
        filename = 'feedback.csv'
        if os.path.isfile(filename):
            try:
                os.remove(filename)
                print(f"File {filename} has been successfully deleted.")
            except Exception as e:
                print(f"Error occurred while deleting file {filename}: {e}")
        else:
            print(f"No such file {filename} in the current directory.")
    
    if feedback:
        with gr.Blocks() as ChatUI:
            chatbot = gr.Chatbot(value = [], elem_id = 'chatbot')
            with gr.Row():
                with gr.Column(scale = 100):
                    msg = gr.Textbox(
                        show_label = False,
                        placeholder = 'Enter Text and Press Enter'
                    )

            with gr.Row():
                with gr.Column():
                    binary = gr.Radio(['Good Response', 'Bad Response'],
                    label = 'Was this a good response?', 
                    value = None)

            with gr.Row():
                with gr.Column(scale = 100):
                    correction = gr.Textbox(
                        show_label = True,
                        label = 'Correction (optional)',
                        placeholder = 'Enter your correction here'
                    )

            with gr.Row():
                with gr.Column(scale = 100):
                    submit_button = gr.Button(value = 'Submit Feedback')
            with gr.Row():
                with gr.Column(scale = 3):
                    download_button = gr.Button(value = 'Download Feedback')
                with gr.Column(scale = 1):
                    delete_button = gr.Button(value = 'Clear Feedback')
            
            msg.submit(respond, [msg, chatbot], [msg, chatbot])
            binary.change(fn = lambda choice: binary_feedback_handler(choice))
            correction.change(fn = lambda correction: correction_feedback_handler(correction), inputs = [correction])
            submit_button.click(fn = submit_feedback)
            download_button.click(fn = save_to_downloads)
            delete_button.click(fn = delete_csv)

        ChatUI.launch()

    else:
        with gr.Blocks() as ChatUI_without_feedback:
            chatbot = gr.Chatbot(value = [], elem_id = 'chatbot')
            with gr.Row():
                with gr.Column(scale = 100):
                    msg = gr.Textbox(
                        show_label = False,
                        placeholder = 'Enter Text and Press Enter'
                    )

            msg.submit(respond, [msg, chatbot], [msg, chatbot])

        ChatUI_without_feedback.launch()

if __name__ == '__main__':
    deploy()
    