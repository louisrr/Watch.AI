export interface VideoProcessingProps {
  videoId: string;
  onProcessingComplete: (processedVideoUrl: string) => void;
}

export interface VideoProcessingResponse {
  data: {
    processedVideoUrl: string;
  };
}

export interface VideoProcessingError {
  response?: {
    data?: {
      detail: string;
    };
  };
}
