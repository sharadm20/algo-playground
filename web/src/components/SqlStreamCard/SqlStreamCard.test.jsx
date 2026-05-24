import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import SqlStreamCard from './SqlStreamCard';

const basicQuery = {
  id: 'filter-basic',
  category: 'Filtering & Conditionals',
  difficulty: 'beginner',
  title: 'Find Customers with High Purchase Amounts',
  description: 'Filter customers who made purchases above a threshold',
  domain: 'ecommerce',
  sqlQuery: 'SELECT * FROM customers WHERE total_purchases > 1000',
  javaStreamCode: 'customers.stream().filter(c -> c.getTotalPurchases() > 1000)',
  explanation: 'Both approaches filter records based on a condition.',
  output: 'customer_id | name\n1 | Alice',
};

const mockSchema = {
  ddl: 'CREATE TABLE customers (...);',
  sampleData: 'INSERT INTO customers VALUES (...);',
  javaModels: 'public class Customer { }',
};

describe('SqlStreamCard', () => {
  it('renders title and description collapsed by default', () => {
    render(<SqlStreamCard query={basicQuery} schema={mockSchema} />);
    expect(screen.getByText('Find Customers with High Purchase Amounts')).toBeInTheDocument();
    expect(screen.getByText('Filter customers who made purchases above a threshold')).toBeInTheDocument();
  });

  it('renders difficulty badge', () => {
    render(<SqlStreamCard query={basicQuery} schema={mockSchema} />);
    expect(screen.getByText('beginner')).toBeInTheDocument();
  });

  it('renders category label', () => {
    render(<SqlStreamCard query={basicQuery} schema={mockSchema} />);
    expect(screen.getByText('Filtering & Conditionals')).toBeInTheDocument();
  });

  it('shows SQL and Java code after expanding', () => {
    render(<SqlStreamCard query={basicQuery} schema={mockSchema} />);
    fireEvent.click(screen.getByRole('button', { name: /show details/i }));
    expect(screen.getByText(/SELECT \* FROM customers/)).toBeInTheDocument();
    expect(screen.getByText(/customers\.stream\(\)/)).toBeInTheDocument();
  });

  it('hides code after re-clicking header', () => {
    render(<SqlStreamCard query={basicQuery} schema={mockSchema} />);
    fireEvent.click(screen.getByRole('button', { name: /show details/i }));
    expect(screen.getByText(/SELECT \* FROM customers/)).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /hide details/i }));
    expect(screen.queryByText(/SELECT \* FROM customers/)).not.toBeInTheDocument();
  });

  it('renders schema toggle and shows schema sections', () => {
    render(<SqlStreamCard query={basicQuery} schema={mockSchema} />);
    fireEvent.click(screen.getByRole('button', { name: /show details/i }));
    fireEvent.click(screen.getByText('Show Schema & Models'));
    expect(screen.getByText('Database Schema')).toBeInTheDocument();
    expect(screen.getByText('Sample Data')).toBeInTheDocument();
    expect(screen.getByText('Java Models')).toBeInTheDocument();
  });

  it('shows DDL when clicking Database Schema section', () => {
    render(<SqlStreamCard query={basicQuery} schema={mockSchema} />);
    fireEvent.click(screen.getByRole('button', { name: /show details/i }));
    fireEvent.click(screen.getByText('Show Schema & Models'));
    fireEvent.click(screen.getByText(/Database Schema/));
    expect(screen.getByText(/CREATE TABLE customers/)).toBeInTheDocument();
  });

  it('handles null query gracefully', () => {
    const { container } = render(<SqlStreamCard query={null} schema={null} />);
    expect(container.innerHTML).toBe('');
  });

  it('shows copy buttons on code blocks', () => {
    render(<SqlStreamCard query={basicQuery} schema={mockSchema} />);
    fireEvent.click(screen.getByRole('button', { name: /show details/i }));
    const copyButtons = screen.getAllByText('Copy');
    expect(copyButtons.length).toBeGreaterThanOrEqual(2);
  });

  it('supports keyboard activation with Enter key', () => {
    render(<SqlStreamCard query={basicQuery} schema={mockSchema} />);
    const header = screen.getByRole('button', { name: /show details/i });
    fireEvent.keyDown(header, { key: 'Enter' });
    expect(screen.getByText(/SELECT \* FROM customers/)).toBeInTheDocument();
  });
});
