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
});
