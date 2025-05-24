import React from 'react';
import Navbar from '../components/Navbar';

const TransactionPage = () => {
  return (
    <>
      <Navbar />
      <div className="page-container">
        <h2>All Transactions</h2>
        {/* Future: Transaction Table and Filters */}
      </div>
    </>
  );
};

export default TransactionPage;
