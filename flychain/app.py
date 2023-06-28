from agent import create_agent
import gradio as gr
import click


@click.command()
@click.option('--model', '-m', default = 'gpt-4')
@click.option('--history/--no-history', default = True)
def deploy(model, history)
    agent = create_agent(model = model, chat_history = history)

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
