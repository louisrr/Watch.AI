export interface CreateUserProps {
  email: string;
  password: string;
  message: string;
}

export interface CreateUserResponse {
  data: {
    message: string;
  };
}

export interface CreateUserError {
  response?: {
    data?: {
      detail: string;
    };
  };
}
