'use client';

import { createContext, useContext, type KeyboardEvent, type ReactNode } from 'react';

type ToggleContextValue = { type: 'single' | 'multiple'; values: string[]; toggle: (value: string) => void };
const ToggleContext = createContext<ToggleContextValue | null>(null);

type ToggleGroupProps = {
  type: 'single' | 'multiple';
  value: string | string[];
  onValueChange: (value: string | string[]) => void;
  label: string;
  className?: string;
  children: ReactNode;
};

export function LucianToggleGroup({ type, value, onValueChange, label, className, children }: ToggleGroupProps) {
  const values = Array.isArray(value) ? value : value ? [value] : [];
  function toggle(next: string) {
    if (type === 'single') { if (!values.includes(next)) onValueChange(next); return; }
    onValueChange(values.includes(next) ? values.filter((item) => item !== next) : [...values, next]);
  }
  function moveFocus(event: KeyboardEvent<HTMLDivElement>) {
    if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(event.key)) return;
    const buttons = Array.from(event.currentTarget.querySelectorAll<HTMLButtonElement>('button:not(:disabled)'));
    const current = buttons.indexOf(document.activeElement as HTMLButtonElement);
    if (current < 0 || buttons.length < 2) return;
    event.preventDefault();
    const direction = event.key === 'ArrowLeft' || event.key === 'ArrowUp' ? -1 : 1;
    buttons[(current + direction + buttons.length) % buttons.length]?.focus();
  }
  return <ToggleContext.Provider value={{ type, values, toggle }}><div className={className} role={type === 'single' ? 'radiogroup' : 'group'} aria-label={label} onKeyDown={moveFocus}>{children}</div></ToggleContext.Provider>;
}

export function LucianToggleItem({ value, label, title, children }: { value: string; label: string; title?: string; children: ReactNode }) {
  const context = useContext(ToggleContext);
  if (!context) throw new Error('LucianToggleItem must be inside LucianToggleGroup');
  const selected = context.values.includes(value);
  return <button type="button" role={context.type === 'single' ? 'radio' : 'checkbox'} aria-checked={selected} aria-label={label} title={title} data-state={selected ? 'on' : 'off'} onClick={() => context.toggle(value)}>{children}</button>;
}
