from agent import create_agent
import gradio as gr
import click


@click.command()
@click.option('--model', '-m', default = 'gpt-4')
@click.option('--history/--no-history', default = True)
@click.option('--temperature', type = int, default = 0)
@click.option('--task', type = str, default = 'text-generation')
@click.option('--huggingface-pipeline-kwargs', type = dict, default = None)
@click.option('--huggingface-model-kwargs', type = dict, default = None)
def deploy(model, history, temperature, task, huggingface_pipeline_kwargs, huggingface_model_kwargs):
    agent = create_agent(model = model, chat_history = history, temperature = temperature, task = task, huggingface_pipeline_kwargs = huggingface_pipeline_kwargs, huggingface_model_kwargs = huggingface_model_kwargs)

    with gr.Blocks() as demo:
        chatbot = gr.Chatbot()
        msg = gr.Textbox()
        clear = gr.ClearButton([msg, chatbot])

        def respond(message, chat_history):
            bot_message = agent.run(message)
            chat_history.append((message, bot_message))
            return "", chat_history

        msg.submit(respond, [msg, chatbot], [msg, chatbot])

    demo.launch()

if __name__ == '__main__':
    deploy()
