export const joyallyTheme = {
  light: {
    background: '#F8F7F3',
    surface: '#FFFDFB',
    surfaceMuted: '#EDF3F1',
    text: '#23393D',
    textSecondary: '#52696B',
    primary: '#63ACA2',
    primaryAction: '#78BEB3',
    onPrimaryAction: '#23393D',
    primaryContainer: '#E1F2EE',
    success: '#356439',
    warning: '#7A5B1E',
    error: '#8E493E',
    border: '#D9E5E2',
    focus: '#57958E',
  },
  dark: {
    background: '#1D3036',
    surface: '#253A40',
    surfaceMuted: '#304A50',
    text: '#F4F8F6',
    textSecondary: '#B8CCDB',
    primary: '#A8D8CF',
    primaryAction: '#A8D8CF',
    onPrimaryAction: '#1D3036',
    primaryContainer: '#315A56',
    success: '#9BC79E',
    warning: '#E5C47B',
    error: '#E5A394',
    border: '#7C999D',
    focus: '#A8D8CF',
  },
  spacing: {
    micro: 4,
    small: 8,
    medium: 16,
    large: 24,
    section: 32,
  },
  radius: {
    control: 10,
    surface: 16,
    expressive: 20,
  },
  typography: {
    body: 16,
    bodyLineHeight: 24,
    label: 14,
    title: 24,
    titleLineHeight: 32,
  },
  breakpoints: {
    compactMax: 599,
    mediumMax: 839,
  },
  minimumTarget: {
    ios: 44,
    android: 48,
  },
  state: {
    disabledOpacity: 0.48,
    pressedOpacity: 0.84,
    focusWidth: 2,
    scrimOpacity: 0.36,
  },
  elevation: {
    resting: 0,
    floating: 4,
    modal: 12,
  },
  motion: {
    fast: 140,
    normal: 200,
    narrative: 550,
  },
} as const;

export type JoyallyTheme = typeof joyallyTheme;
export type JoyallyColorScheme =
  (typeof joyallyTheme)['light' | 'dark'];
