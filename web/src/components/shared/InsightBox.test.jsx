import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import InsightBox from './InsightBox';

describe('InsightBox', () => {
  it('renders title', () => {
    render(<InsightBox title="Key Insights">content</InsightBox>);
    expect(screen.getByText('Key Insights')).toBeInTheDocument();
  });

  it('renders children content', () => {
    render(<InsightBox>Some insight text</InsightBox>);
    expect(screen.getByText('Some insight text')).toBeInTheDocument();
  });

  it('renders default title when not provided', () => {
    render(<InsightBox>content</InsightBox>);
    expect(screen.getByText('Key Insights')).toBeInTheDocument();
  });
});
