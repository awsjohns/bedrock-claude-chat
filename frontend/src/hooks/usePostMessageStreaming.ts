import { Auth } from 'aws-amplify';
import { PostMessageRequest } from '../@types/conversation';
import { create } from 'zustand';

const WS_ENDPOINT: string = import.meta.env.VITE_APP_WS_ENDPOINT;

const usePostMessageStreaming = create<{
  post: (
    input: PostMessageRequest,
    dispatch: (completion: string) => void
  ) => Promise<string>;
}>(() => {
  const post = async (
    input: PostMessageRequest,
    dispatch: (completion: string) => void
  ) => {
    const token = (await Auth.currentSession()).getIdToken().getJwtToken();

    return new Promise<string>((resolve, reject) => {
      const ws = new WebSocket(WS_ENDPOINT);
      let completion = '';
      let conversationId = '';

      ws.onopen = () => {
        ws.send(JSON.stringify({ ...input, token }));
      };

      ws.onmessage = (message) => {
        try {
          const data = JSON.parse(message.data);
  
          console.log(data);

          if (data.outputText) {
            if (completion.endsWith('▍')) {
              completion = completion.slice(0, -1);
            }

            completion += data.outputText; // + (data.stop_reason ? '' : '▍');
            dispatch(completion);
          } else if (data.conversationId) {
            conversationId = data.conversationId;
            ws.close();
          } else {
            ws.close();
            console.error(data);
            throw new Error('An unusual Response is returned.');
          }
        } catch (e) {
          console.error(e);
          reject('An error occurred during inference');
        }
      };

      ws.onerror = (e) => {
        ws.close();
        console.error(e);
        reject('An error occurred during inference');
      };
      ws.onclose = () => {
        resolve(conversationId);
      };
    });
  };

  return {
    post,
  };
});
export default usePostMessageStreaming;
