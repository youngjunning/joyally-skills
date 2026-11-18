import type { Metadata } from 'next';
import type { ReactNode } from 'react';
import './globals.css';
import './themes.css';

export const metadata: Metadata = {
  title: 'Distill Me · 本地数字分身',
  description: '在本机整理判断、进展、资料、待办与文章草稿。',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
