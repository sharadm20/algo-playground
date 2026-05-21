import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import DataTable from './DataTable';

describe('DataTable', () => {
  it('renders all headers', () => {
    const headers = ['Name', 'Age', 'City'];
    render(<DataTable headers={headers} rows={[]} />);
    headers.forEach(h => {
      expect(screen.getByText(h)).toBeInTheDocument();
    });
  });

  it('renders all rows and cells', () => {
    const headers = ['Name', 'Age'];
    const rows = [['Alice', '30'], ['Bob', '25']];
    render(<DataTable headers={headers} rows={rows} />);
    expect(screen.getByText('Alice')).toBeInTheDocument();
    expect(screen.getByText('30')).toBeInTheDocument();
    expect(screen.getByText('Bob')).toBeInTheDocument();
    expect(screen.getByText('25')).toBeInTheDocument();
  });

  it('renders empty table when no headers/rows', () => {
    const { container } = render(<DataTable headers={[]} rows={[]} />);
    const table = container.querySelector('table');
    expect(table).toBeInTheDocument();
    const headers = container.querySelectorAll('th');
    expect(headers.length).toBe(0);
    const rows = container.querySelectorAll('td');
    expect(rows.length).toBe(0);
  });
});
