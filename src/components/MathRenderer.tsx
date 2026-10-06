import React, { useMemo } from 'react';
import { StyleSheet, View, Text, Platform } from 'react-native';
import { WebView } from 'react-native-webview';

interface MathRendererProps {
  latex: string;
  fontSize?: number;
  color?: string;
  backgroundColor?: string;
  displayMode?: boolean;
}

export const MathRenderer: React.FC<MathRendererProps> = ({
  latex,
  fontSize = 16,
  color = '#F3F4F6',
  backgroundColor = 'transparent',
  displayMode = false,
}) => {
  // Sanitize and clean raw dollar signs ($...$ or $$...$$) from input
  const cleanLatexString = useMemo(() => {
    let clean = latex.trim();
    if (clean.startsWith('$$') && clean.endsWith('$$')) {
      clean = clean.slice(2, -2).trim();
    } else if (clean.startsWith('$') && clean.endsWith('$')) {
      clean = clean.slice(1, -1).trim();
    }
    return clean;
  }, [latex]);

  const htmlContent = useMemo(() => {
    const escaped = cleanLatexString
      .replace(/\\/g, '\\\\')
      .replace(/'/g, "\\'")
      .replace(/\n/g, ' ');

    return `
      <!DOCTYPE html>
      <html>
        <head>
          <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
          <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
          <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
          <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
              background-color: ${backgroundColor};
              color: ${color};
              font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
              font-size: ${fontSize}px;
              display: flex;
              align-items: center;
              justify-content: ${displayMode ? 'center' : 'flex-start'};
              padding: 4px 6px;
              overflow: hidden;
            }
            .katex { font-size: 1.08em; color: ${color} !important; }
            .katex-display { margin: 0.3em 0 !important; }
          </style>
        </head>
        <body>
          <div id="math-target"></div>
          <script>
            window.addEventListener('DOMContentLoaded', () => {
              try {
                katex.render('${escaped}', document.getElementById('math-target'), {
                  displayMode: ${displayMode},
                  throwOnError: false,
                  output: 'htmlAndMathml'
                });
              } catch (e) {
                document.getElementById('math-target').innerText = '${escaped}';
              }
            });
          </script>
        </body>
      </html>
    `;
  }, [cleanLatexString, fontSize, color, backgroundColor, displayMode]);

  const estimatedHeight = useMemo(() => {
    const lineCount = (cleanLatexString.match(/\\\\|\n/g) || []).length + 1;
    return displayMode ? Math.max(48, lineCount * (fontSize + 22)) : Math.max(32, lineCount * (fontSize + 10));
  }, [cleanLatexString, fontSize, displayMode]);

  if (Platform.OS === 'web') {
    return (
      <View style={[styles.container, { minHeight: estimatedHeight }]}>
        <Text style={[styles.fallbackText, { fontSize, color }]}>{cleanLatexString}</Text>
      </View>
    );
  }

  return (
    <View style={[styles.container, { minHeight: estimatedHeight }]}>
      <WebView
        originWhitelist={['*']}
        source={{ html: htmlContent }}
        style={[styles.webview, { backgroundColor }]}
        scrollEnabled={false}
        showsVerticalScrollIndicator={false}
        showsHorizontalScrollIndicator={false}
        scalesPageToFit={false}
        javaScriptEnabled={true}
        domStorageEnabled={true}
        androidLayerType="hardware"
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    width: '100%',
    marginVertical: 4,
    borderRadius: 8,
    overflow: 'hidden',
  },
  webview: {
    width: '100%',
    height: '100%',
  },
  fallbackText: {
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
    lineHeight: 22,
  },
});
