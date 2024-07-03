export interface RequestPasswordResetResponse {
  data: {
    message: string;
  };
}

export interface RequestPasswordResetError {
  response?: {
    data?: {
      detail: string;
    };
  };
}
