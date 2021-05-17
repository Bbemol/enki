export enum ToastType {
  ERROR = "error",
  INFO = "info",
}
export interface Toast {
  message: string;
  type: ToastType;
}