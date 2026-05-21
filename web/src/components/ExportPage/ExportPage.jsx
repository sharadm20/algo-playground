import { useState, useCallback } from 'react';
import { useProgress } from '../../hooks/useProgress';
import { studyDays } from '../../data/navigation';
import styles from './ExportPage.module.css';

function generateMarkdown(progress) {
  const lines = [];
  const completed = progress.completedDays;
  const total = studyDays.length;
  const pct = Math.round((completed.length / total) * 100);

  lines.push('# DSA Study Plan — Progress Report');
  lines.push('');
  lines.push(`**Progress:** ${completed.length} / ${total} days completed (${pct}%)`);
  lines.push('');
  lines.push('## Overview');
  lines.push('');
  lines.push('| Day | Title | Status |');
  lines.push('|-----|-------|--------|');

  for (const day of studyDays) {
    const status = completed.includes(day.day) ? '✅ Completed' : '⬜ Pending';
    lines.push(`| ${day.day} | ${day.title} | ${status} |`);
  }

  lines.push('');
  lines.push('## Weekly Breakdown');
  lines.push('');

  const weeks = {};
  for (const day of studyDays) {
    if (!weeks[day.week]) weeks[day.week] = [];
    weeks[day.week].push(day);
  }

  for (const [week, days] of Object.entries(weeks)) {
    const weekCompleted = days.filter(d => completed.includes(d.day)).length;
    lines.push(`### Week ${week} (${weekCompleted}/${days.length} days)`);
    lines.push('');
    for (const day of days) {
      const status = completed.includes(day.day) ? '✅' : '⬜';
      lines.push(`- ${status} **Day ${day.day}:** ${day.title} (${day.topic})`);
    }
    lines.push('');
  }

  return lines.join('\n');
}

export default function ExportPage() {
  const { progress, exportProgress } = useProgress();
  const [copied, setCopied] = useState(false);

  const markdown = generateMarkdown(progress);
  const jsonData = JSON.stringify(exportProgress(), null, 2);

  const copyToClipboard = useCallback(async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      const ta = document.createElement('textarea');
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  }, []);

  const downloadFile = useCallback((content, filename, mime) => {
    const blob = new Blob([content], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }, []);

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>Export Progress</h1>
      <p className={styles.subtitle}>Download or copy your progress report to share with others.</p>

      <div className={styles.grid}>
        <div className={styles.card}>
          <h3>Markdown Report</h3>
          <div className={styles.preview}>{markdown}</div>
          <div>
            <button className={styles.btn} onClick={() => downloadFile(markdown, 'dsa-progress.md', 'text/markdown')}>
              {'\u2B07'} Download .md
            </button>
            <button className={`${styles.btn} ${styles.btnSecondary}`} onClick={() => copyToClipboard(markdown)}>
              {copied ? '\u2705' : '\uD83D\uDCCB'} Copy
            </button>
          </div>
        </div>

        <div className={styles.card}>
          <h3>JSON Data</h3>
          <div className={styles.preview}>{jsonData}</div>
          <div>
            <button className={styles.btn} onClick={() => downloadFile(jsonData, 'dsa-progress.json', 'application/json')}>
              {'\u2B07'} Download .json
            </button>
            <button className={`${styles.btn} ${styles.btnSecondary}`} onClick={() => copyToClipboard(jsonData)}>
              {copied ? '\u2705' : '\uD83D\uDCCB'} Copy
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
