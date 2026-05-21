import { useState, useEffect, useRef } from 'react';
import { EditorView, basicSetup } from 'codemirror';
import { EditorState } from '@codemirror/state';
import { python } from '@codemirror/lang-python';
import { javascript } from '@codemirror/lang-javascript';
import { rust } from '@codemirror/lang-rust';
import { java } from '@codemirror/lang-java';
import { cpp } from '@codemirror/lang-cpp';
import { oneDark } from '@codemirror/theme-one-dark';
import { useCodeRunner } from '../../hooks/useCodeRunner';
import { useTheme } from '../../context/ThemeContext';
import OutputPanel from './OutputPanel';
import styles from './CodePlayground.module.css';

const LANG_MODES = {
  python, javascript, js: javascript,
  rust, java, c: cpp, cpp, go: javascript,
};

const LANG_OPTIONS = [
  { value: 'python', label: 'Python' },
  { value: 'rust', label: 'Rust' },
  { value: 'javascript', label: 'JavaScript' },
  { value: 'java', label: 'Java' },
  { value: 'c', label: 'C' },
  { value: 'go', label: 'Go' },
];

export default function CodePlayground({ initialCode = '', language = 'python' }) {
  const editorRef = useRef(null);
  const viewRef = useRef(null);
  const [code, setCode] = useState(initialCode);
  const [lang, setLang] = useState(language);
  const [resetCode] = useState(initialCode);
  const { running, output, error, run } = useCodeRunner();
  const { theme } = useTheme();

  useEffect(() => {
    if (!editorRef.current) return;
    if (viewRef.current) viewRef.current.destroy();

    const langMode = LANG_MODES[lang] || python;
    const extensions = [basicSetup, langMode()];
    if (theme === 'dark') extensions.push(oneDark);

    const state = EditorState.create({
      doc: code,
      extensions,
    });

    viewRef.current = new EditorView({
      state,
      parent: editorRef.current,
      dispatch: (tr) => {
        viewRef.current.update([tr]);
        if (tr.docChanged) setCode(viewRef.current.state.doc.toString());
      },
    });

    return () => viewRef.current?.destroy();
  }, [lang, theme]);

  return (
    <div className={styles.wrapper}>
      <div className={styles.toolbar}>
        <select
          className={styles.langSelect}
          value={lang}
          onChange={e => setLang(e.target.value)}
        >
          {LANG_OPTIONS.map(o => (
            <option key={o.value} value={o.value}>{o.label}</option>
          ))}
        </select>
        <button className={styles.runBtn} disabled={running} onClick={() => run(code, lang)}>
          {running ? 'Running...' : '\u25B6 Run'}
        </button>
        <button className={styles.resetBtn} onClick={() => setCode(resetCode)}>
          {'\u21BA Reset'}
        </button>
      </div>
      <div className={styles.editor} ref={editorRef} />
      <OutputPanel output={output} error={error} running={running} />
    </div>
  );
}
