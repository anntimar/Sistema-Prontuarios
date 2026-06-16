const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

type RequestOptions = {
  token?: string;
  body?: unknown;
  form?: FormData;
  method?: "GET" | "POST" | "PATCH" | "DELETE";
};

export async function apiRequest<T>(
  path: string,
  { token, body, form, method = "GET" }: RequestOptions = {},
): Promise<T> {
  const headers = new Headers();
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }
  if (body !== undefined) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(`${API_URL}${path}`, {
    method,
    headers,
    body: form ?? (body === undefined ? undefined : JSON.stringify(body)),
  });

  const contentType = response.headers.get("content-type") ?? "";
  const data = contentType.includes("application/json") ? await response.json() : null;

  if (!response.ok) {
    const message = data?.error?.message ?? data?.detail ?? "Erro ao chamar a API.";
    throw new ApiError(message, response.status);
  }

  return data as T;
}

export async function apiDownload(
  path: string,
  { token }: { token?: string } = {},
): Promise<Blob> {
  const headers = new Headers();
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_URL}${path}`, { headers });

  if (!response.ok) {
    const contentType = response.headers.get("content-type") ?? "";
    const data = contentType.includes("application/json") ? await response.json() : null;
    const message = data?.error?.message ?? data?.detail ?? "Erro ao baixar arquivo.";
    throw new ApiError(message, response.status);
  }

  return response.blob();
}

export function getApiUrl() {
  return API_URL;
}
