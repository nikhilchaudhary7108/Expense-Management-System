import React from 'react';
import Navbar from '../components/Navbar';

const ExpensePage = () => {
  return (
    <>
      <Navbar />
      <div className="page-container">
        <h2>All Expenses</h2>
        {/* Future implementation: List all expenses with filters */}
      </div>
    </>
  );
};

export default ExpensePage;
