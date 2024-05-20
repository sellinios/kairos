// src/types/custom.d.ts

declare module '*.png' {
  const value: string;
  export default value;
}

declare module '*.svg' {
  const content: any;
  export default content;
}
