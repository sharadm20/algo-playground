import { createBrowserRouter, Navigate } from 'react-router-dom';
import Layout from './components/Layout/Layout';
import HomePage from './components/HomePage/HomePage';
import DayPage from './components/DayPage/DayPage';
import ExportPage from './components/ExportPage/ExportPage';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'day/:dayId', element: <DayPage /> },
      { path: 'export', element: <ExportPage /> },
      { path: '*', element: <Navigate to="/" replace /> },
    ],
  },
]);

export default router;
