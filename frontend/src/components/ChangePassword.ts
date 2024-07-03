export interface ChangePasswordParams {
  unique_hash: string;
}

export interface ChangePasswordResponse {
  data: {
    message: string;
  };
}

export interface ChangePasswordError {
  response?: {
    data?: {
      detail: string;
    };
  };
}
