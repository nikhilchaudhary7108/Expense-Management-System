import React from 'react';
import Navbar from '../components/Navbar';

const IncomePage = () => {
  return (
    <>
      <Navbar />
      <div className="page-container">
        <h2>All Incomes</h2>
        {/* Future implementation: List all incomes with filters */}
      </div>
    </>
  );
};

export default IncomePage;
