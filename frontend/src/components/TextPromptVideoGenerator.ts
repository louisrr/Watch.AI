export interface TextPromptVideoGeneratorResponse {
  data: {
    video_url: string;
  };
}

export interface TextPromptVideoGeneratorError {
  response?: {
    data?: {
      detail: string;
    };
  };
}
