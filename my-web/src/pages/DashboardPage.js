import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './DashboardPage.css';
import { useLocation, useNavigate } from 'react-router-dom';
import defaultAvatar from './default-avatar.png';


export default function DashboardPage() {
  const location = useLocation();
  const navigate = useNavigate();

  const [user] = useState(location.state?.user || {});
  const [transactions, setTransactions] = useState([]);
  const [allTransactions, setAllTransactions] = useState([]);
  const [error, setError] = useState('');
  const [showExpenseForm, setShowExpenseForm] = useState(false);
  const [showIncomeForm, setShowIncomeForm] = useState(false);
  const [showProfile, setShowProfile] = useState(false);
  const [showBudgetForm, setShowBudgetForm] = useState(false);
  const [showCategoryForm, setShowCategoryForm] = useState(false);

  const [expenseAmount, setExpenseAmount] = useState('');
  const [expenseCategory, setExpenseCategory] = useState('');
  const [expenseDescription, setExpenseDescription] = useState('');

  const [incomeAmount, setIncomeAmount] = useState('');
  const [incomeSource, setIncomeSource] = useState('');
  const [incomeDescription, setIncomeDescription] = useState('');

  const [budgetName, setBudgetName] = useState('');
const [budgetAmount, setBudgetAmount] = useState('');
const [budgetStartDate, setBudgetStartDate] = useState('');
const [budgetEndDate, setBudgetEndDate] = useState('');
const [budgetCategory, setBudgetCategory] = useState('');

const [showBudgetAnalysis, setShowBudgetAnalysis] = useState(false);
const [budgetAnalysisData, setBudgetAnalysisData] = useState([]);

const [categories, setCategories] = useState([]);
const [newCategory, setNewCategory] = useState('');

const [successMessage, setSuccessMessage] = useState('');


  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log("Fetching transactions for user ID:", user.user_id); // Debugging
        const res = await axios.get(`http://localhost:5000/transactions/${user.user_id}`);
        console.log(res.data); // Check if the response contains the expected data
        setTransactions(res.data);
        setAllTransactions(res.data);
  
        // const categoryRes = await axios.get(`http://localhost:5000/categories/${user.user_id}`);
        // setCategories(categoryRes.data);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError('');
      }
    };
  
    if (user.user_id) {
      fetchData();
    }
  }, [user.user_id]);

  useEffect(() => {
    const fetchCategory = async () => {
      try {
        
  
        const categoryRes = await axios.get(`http://localhost:5000/categories/${user.user_id}`);
        setCategories(categoryRes.data);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError('');
      }
    };
  
    if (user.user_id) {
      fetchCategory();
    }
  }, [user.user_id]);
  
  const handleAddExpense = async (e) => {
    e.preventDefault();
    const newExpense = {
      user_id: user.user_id,
      amount: expenseAmount,
      category_name: expenseCategory,
      description: expenseDescription,
      date: new Date().toISOString().split('T')[0],
    };
    console.log(newExpense); // Debugging
    try {
      const response = await axios.post('http://localhost:5000/add-expense', newExpense);
      console.log(response.data); // Debugging
      const savedExpense = response.data.expense;
  
      setTransactions([...transactions, savedExpense]);
      setAllTransactions([...allTransactions, savedExpense]);
  
      setShowExpenseForm(false);
      setExpenseAmount('');
      setExpenseCategory('');
      setExpenseDescription('');
      setSuccessMessage('Expense added successfully!');
      setTimeout(() => {
        setSuccessMessage('');
      }, 3000);
    } catch (err) {
      console.error('Error adding expense:', err);
      setError(err.response?.data?.error || 'Failed to add expense');
    }
  };

  const handleAddIncome = async (e) => {
    e.preventDefault();
    try {
      const newIncome = {
        user_id: user.user_id,
        amount: incomeAmount,
        source: incomeSource,
        description: incomeDescription,
        date: new Date().toISOString().split('T')[0],
      };

      const response = await axios.post('http://localhost:5000/add-income', newIncome);
      const savedIncome = response.data.income;

      setTransactions([...transactions, savedIncome]);
      setAllTransactions([...allTransactions, savedIncome]);

      setShowIncomeForm(false);
      setIncomeAmount('');
      setIncomeSource('');
      setIncomeDescription('');
      setSuccessMessage('Income added successfully!');
      setTimeout(() => {
        setSuccessMessage('');
      }, 3000);
    } catch (err) {
      console.error('Error adding income:', err);
      setError(err.response?.data?.error || 'Failed to add income');
    }
  };
  
  const handleAddCategory = async (e) => {
    e.preventDefault();
  
    // Check if the category name or user ID is missing
    if (!newCategory.trim()) {
      alert("Please provide a category name.");
      return;
    }
  
    if (!user?.user_id) {
      alert("User ID is missing or invalid. Please log in.");
      return;
    }
  
    try {
      // Make the request to add the category
      const response = await axios.post('http://localhost:5000/add-category', {
        category_name: newCategory,
        user_id: user.user_id,
      });
  
      const createdCategory = response.data;
      
      // Fetch updated categories
      const categoryRes = await axios.get(`http://localhost:5000/categories/${user.user_id}`);
      setCategories(categoryRes.data.map(cat => ({
        name: cat.category_name || cat.name,
        category_id: cat.category_id,
      })));
  
      // Update expense category with the new category
      if (showExpenseForm) {
        setExpenseCategory(createdCategory.name);
      }
      setNewCategory('');
      // setExpenseCategory(createdCategory.name);
      setSuccessMessage('Category added successfully!');
      setTimeout(() => {
        setSuccessMessage('');
      }, 3000);
  
    } catch (err) {
      // Handle error and log detailed message
      console.error('Error adding category:', err);
      setError(err.response?.data?.error || 'Failed to add category');
    }
  };
  

  const handleSetBudget = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/add-budget', {
        user_id: user.user_id,
        name: budgetName,
        amount: budgetAmount,
        start_date: budgetStartDate,
        end_date: budgetEndDate,
        category_name: budgetCategory,
      });
  
      setShowBudgetForm(false);
      setBudgetName('');
      setBudgetAmount('');
      setBudgetStartDate('');
      setBudgetEndDate('');
      setBudgetCategory('');
      setSuccessMessage('Budget created successfully!');
      setTimeout(() => {
        setSuccessMessage('');
      }, 3000);
    } catch (err) {
      console.error('Error setting budget:', err);
      setError(err.response?.data?.error || 'Failed to set budget');
    }
  };

  
  useEffect(() => {
    if (showBudgetAnalysis) {
      handleBudgetAnalysis();
    }
  }, [showBudgetAnalysis]);
  
  const handleBudgetAnalysis = async () => {
    try {
      const budgetRes = await axios.get(`http://localhost:5000/budget-summary/${user.user_id}`);
      const budgets = budgetRes.data;
  
      // Analysis to calculate the spent and left amounts for each budget
      const analysis = budgets.map(budget => {
        const spent = budget.total_spent;
        const left = budget.remaining;
  
        return {
          budget_name: budget.budget_name,
          category_name: budget.category_name,
          budgeted: budget.budget_amount,
          spent: spent,
          left: left
        };
      });
  
      setBudgetAnalysisData(analysis);
    } catch (err) {
      console.error('Error fetching budget analysis:', err);
      setError('Failed to load budget analysis');
    }
  };
  
  
  

  const handleFilterChange = (e) => {
    const selected = e.target.value;
    if (selected) {
      const filtered = allTransactions.filter(t => t.category_name === selected);
      setTransactions(filtered);
    } else {
      setTransactions(allTransactions);
    }
  };

  const handleLogout = () => {
    navigate('/');
  };

  return (
    <div className="dashboard-container">

      
      <div className="top-bar">
        <h2>Welcome, {user.username}</h2>
        <div className="profile-section">
        <div className="avatar" onClick={() => setShowProfile(!showProfile)}>
  <img src={defaultAvatar} alt="Profile" />
</div>


{showProfile && (
  <div className="profile-dropdown animated-dropdown">
    <p><strong>User ID:</strong> {user.user_id}</p>
    <p><strong>Email:</strong> {user.email}</p>
    <p><strong>Mobile:</strong> {user.mobile_no}</p>
    <button onClick={handleLogout} className="logout-btn">Logout</button>
  </div>
)}

        </div>
      </div>

      <div className="actions">
        <button onClick={() => setShowExpenseForm(!showExpenseForm)}>Add Expense</button>
        <button onClick={() => setShowIncomeForm(!showIncomeForm)}>Add Income</button>
        <button onClick={() => setShowBudgetForm(!showBudgetForm)}>Set Budget</button>
        <button onClick={() => setShowCategoryForm(!showCategoryForm)}>Add Category</button>
        <button onClick={() => setShowBudgetAnalysis(!showBudgetAnalysis)}>View Budget Analysis</button>
        <button onClick={() => navigate("/graphical-view", { state: { user: user } })}>Graphical View</button>

        
      </div>

      {successMessage && <p className="success-message">{successMessage}</p>}
      {showCategoryForm && (
        <div className="form-container">
          <h3>Add New Category</h3>
          <form onSubmit={handleAddCategory}>
            <input type="text" value={newCategory} onChange={(e) => setNewCategory(e.target.value)} placeholder="Category Name" required />
            <button type="submit">Add Category</button>
            <button type="button" onClick={() => setShowCategoryForm(false)}>Cancel</button>
          </form>
        </div>
      )}

{showBudgetForm && (
  <div className="form-container">
    <h3>Set Budget</h3>


    <form onSubmit={handleSetBudget}>
      <input
        type="text"
        value={budgetName}
        onChange={(e) => setBudgetName(e.target.value)}
        placeholder="Budget Name"
        required
      />
      <input
        type="number"
        value={budgetAmount}
        onChange={(e) => setBudgetAmount(e.target.value)}
        placeholder="Budget Amount"
        required
      />
      <input
        type="date"
        value={budgetStartDate}
        onChange={(e) => setBudgetStartDate(e.target.value)}
        required
      />
      <input
        type="date"
        value={budgetEndDate}
        onChange={(e) => setBudgetEndDate(e.target.value)}
        required
      />
      <select
        value={budgetCategory}
        onChange={(e) => setBudgetCategory(e.target.value)}
        required
      >
        <option value="">Select Category</option>
        {categories.map(cat => (
          <option key={cat.category_id} value={cat.name}>{cat.name}</option>
        ))}
      </select>
      <button type="submit">Set Budget</button>
      <button type="button" onClick={() => setShowBudgetForm(false)}>Cancel</button>
    </form>
  </div>
)}

{showBudgetAnalysis && (
  <div className="budget-analysis-container">
    <h3>Budget Analysis</h3>
    <button onClick={() => setShowBudgetAnalysis(false)} className="close-button">
        Close
      </button>
    {budgetAnalysisData.length === 0 ? (
      <p>No budgets found.</p>
    ) : (
      <table>
        <thead>
          <tr>
            <th>Budget Name</th>
            <th>Category</th>
            <th>Budgeted</th>
            <th>Spent</th>
            <th>Left</th>
          </tr>
        </thead>
        <tbody>
          {budgetAnalysisData.map((b, i) => (
            <tr key={i}>
              <td>{b.budget_name}</td>
              <td>{b.category_name}</td>
              <td>₹{b.budgeted}</td>
              <td>₹{b.spent}</td>
              <td style={{ color: b.left < 0 ? 'red' : 'green' }}>
                ₹{b.left}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    )}
  </div>
)}


      {showExpenseForm && (
        <div className="form-container">
          <h3>Add Expense</h3>
          

          <form onSubmit={handleAddExpense}>
            <input type="number" value={expenseAmount} onChange={(e) => setExpenseAmount(e.target.value)} placeholder="Amount" required />
            <select value={expenseCategory} onChange={(e) => setExpenseCategory(e.target.value)} required>
              <option value="">Select Category</option>
              {categories.map(cat => (
                <option key={cat.category_id} value={cat.name}>{cat.name}</option>
              ))}
              <option value="add-new">Add New Category</option>
            </select>
            {expenseCategory === 'add-new' && (
              <div>
                <input type="text" value={newCategory} onChange={(e) => setNewCategory(e.target.value)} placeholder="New Category" />
                <button type="button" onClick={handleAddCategory}>Add Category</button>
              </div>
            )}
            <textarea value={expenseDescription} onChange={(e) => setExpenseDescription(e.target.value)} placeholder="Description" required />
            <button type="submit">Add Expense</button>
            <button type="button" onClick={() => setShowExpenseForm(false)}>Cancel</button>
          </form>
        </div>
      )}

      {showIncomeForm && (
        <div className="form-container">
          <h3>Add Income</h3>

          <form onSubmit={handleAddIncome}>
            <input type="number" value={incomeAmount} onChange={(e) => setIncomeAmount(e.target.value)} placeholder="Amount" required />
            <input type="text" value={incomeSource} onChange={(e) => setIncomeSource(e.target.value)} placeholder="Source" required />
            <textarea value={incomeDescription} onChange={(e) => setIncomeDescription(e.target.value)} placeholder="Description" required />
            <button type="submit">Add Income</button>
            <button type="button" onClick={() => setShowIncomeForm(false)}>Cancel</button>
          </form>
        </div>
      )}

      <div className="transactions">
        <h3>Past Transactions</h3>
        {error && <p className="error">{error}</p>}

        <label htmlFor="categoryFilter">Filter by Category:</label>
        <select id="categoryFilter" onChange={handleFilterChange}>
          <option value="">All Categories</option>
          {categories.map(cat => (
            <option key={cat.category_id} value={cat.name}>{cat.name}</option>
          ))}
        </select>

        {transactions.length === 0 ? (
          <p>No transactions yet.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Amount</th>
                <th>Type</th>
                <th>Category</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {transactions.map((t, index) => (
                <tr key={index}>
                  <td>{new Date(t.date).toLocaleDateString()}</td>
                  <td>₹{t.amount}</td>
                  <td>{t.type}</td>
                  <td>{t.category_name || t.source || '-'}</td>
                  <td>{t.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        {/* Pie Chart */}
    
      </div>
    </div>
  );
}


// import React, { useEffect, useState } from 'react';
// import axios from 'axios';
// import './DashboardPage.css';
// import { useLocation, useNavigate } from 'react-router-dom';

// export default function DashboardPage() {
//   const location = useLocation();
//   const navigate = useNavigate();

//   // Get user data from route state
//   const [user] = useState(location.state?.user || {});
//   const [transactions, setTransactions] = useState([]);
//   const [error, setError] = useState('');
//   const [showExpenseForm, setShowExpenseForm] = useState(false);
//   const [showIncomeForm, setShowIncomeForm] = useState(false);
//   const [expenseAmount, setExpenseAmount] = useState('');
//   const [expenseCategory, setExpenseCategory] = useState('');
//   const [expenseDescription, setExpenseDescription] = useState('');
//   const [incomeAmount, setIncomeAmount] = useState('');
//   const [incomeSource, setIncomeSource] = useState('');
//   const [incomeDescription, setIncomeDescription] = useState('');
//   const [categories, setCategories] = useState([]);
//   const [newCategory, setNewCategory] = useState(''); // For new custom category

//   // Fetch transactions and categories
//   useEffect(() => {
//     const fetchData = async () => {
//       try {
//         // Fetch transactions
//         const res = await axios.get(`http://localhost:5000/transactions/${user.user_id}`);
//         console.log('Transactions data:', res.data);
//         setTransactions(res.data);

//         // Fetch categories (for expense form)
//         const categoryRes = await axios.get(`http://localhost:5000/categories`);
//         setCategories(categoryRes.data); // Assuming you have a route to fetch categories
//       } catch (err) {
//         console.error('Error fetching data:', err);
//         setError('Failed to load data');
//       }
//     };

//     if (user.user_id) {
//       fetchData();
//     }
//   }, [user.user_id]);

//   // Add expense handler
//   const handleAddExpense = async (e) => {
//     e.preventDefault();
//     try {
//       await axios.post('http://localhost:5000/add-expense', {
//         user_id: user.user_id,
//         amount: expenseAmount,
//         category_name: expenseCategory,
//         description: expenseDescription,
//         date: new Date().toISOString(),
//       });
//       // Refresh transactions after adding expense
//       setShowExpenseForm(false); // Close the form after submitting
//       setExpenseAmount('');
//       setExpenseCategory('');
//       setExpenseDescription('');
//       setTransactions([...transactions, { amount: expenseAmount, category_name: expenseCategory, description: expenseDescription }]); // Update local state for immediate feedback
//     } catch (err) {
//       console.error('Error adding expense:', err);
//       setError('Failed to add expense');
//     }
//   };

//   // Add income handler
//   const handleAddIncome = async (e) => {
//     e.preventDefault();
//     try {
//       await axios.post('http://localhost:5000/add-income', {
//         user_id: user.user_id,
//         amount: incomeAmount,
//         source: incomeSource,
//         description: incomeDescription,
//         date: new Date().toISOString(),
//       });
//       // Refresh transactions after adding income
//       setShowIncomeForm(false); // Close the form after submitting
//       setIncomeAmount('');
//       setIncomeSource('');
//       setIncomeDescription('');
//       setTransactions([...transactions, { amount: incomeAmount, source: incomeSource, description: incomeDescription }]); // Update local state for immediate feedback
//     } catch (err) {
//       console.error('Error adding income:', err);
//       setError('Failed to add income');
//     }
//   };

//   // Add custom category handler
//   const handleAddCategory = async (e) => {
//     e.preventDefault();
//     if (!newCategory.trim()) return; // Do not add empty category

//     try {
//       // Send the new category to the server
//       await axios.post('http://localhost:5000/add-category', {
//         name: newCategory,
//       });

//       // Update local categories
//       setCategories([...categories, { name: newCategory }]);
//       setNewCategory(''); // Clear input after adding
//     } catch (err) {
//       console.error('Error adding category:', err);
//       setError('Failed to add category');
//     }
//   };

//   // Toggle forms
//   const toggleExpenseForm = () => setShowExpenseForm(!showExpenseForm);
//   const toggleIncomeForm = () => setShowIncomeForm(!showIncomeForm);

//   return (
//     <div className="dashboard-container">
//       <h2>Welcome, {user.username}</h2>

//       <div className="actions">
//         <button onClick={toggleExpenseForm}>Add Expense</button>
//         <button onClick={toggleIncomeForm}>Add Income</button>
//       </div>

//       {/* Expense Form */}
//       {showExpenseForm && (
//         <div className="form-container">
//           <h3>Add Expense</h3>
//           <form onSubmit={handleAddExpense}>
//             <input
//               type="number"
//               value={expenseAmount}
//               onChange={(e) => setExpenseAmount(e.target.value)}
//               placeholder="Amount"
//               required
//             />
//             <select
//               value={expenseCategory}
//               onChange={(e) => setExpenseCategory(e.target.value)}
//               required
//             >
//               <option value="">Select Category</option>
//               {categories.map((category) => (
//                 <option key={category.category_id} value={category.name}>
//                   {category.name}
//                 </option>
//               ))}
//               <option value="add-new">Add New Category</option> {/* Option to add new category */}
//             </select>
//             {expenseCategory === 'add-new' && (
//               <div>
//                 <input
//                   type="text"
//                   value={newCategory}
//                   onChange={(e) => setNewCategory(e.target.value)}
//                   placeholder="Enter New Category"
//                 />
//                 <button type="button" onClick={handleAddCategory}>
//                   Add Category
//                 </button>
//               </div>
//             )}
//             <textarea
//               value={expenseDescription}
//               onChange={(e) => setExpenseDescription(e.target.value)}
//               placeholder="Description"
//               required
//             />
//             <button type="submit">Add Expense</button>
//             <button type="button" onClick={toggleExpenseForm}>
//               Cancel
//             </button>
//           </form>
//         </div>
//       )}

//       {/* Income Form */}
//       {showIncomeForm && (
//         <div className="form-container">
//           <h3>Add Income</h3>
//           <form onSubmit={handleAddIncome}>
//             <input
//               type="number"
//               value={incomeAmount}
//               onChange={(e) => setIncomeAmount(e.target.value)}
//               placeholder="Amount"
//               required
//             />
//             <input
//               type="text"
//               value={incomeSource}
//               onChange={(e) => setIncomeSource(e.target.value)}
//               placeholder="Source"
//               required
//             />
//             <textarea
//               value={incomeDescription}
//               onChange={(e) => setIncomeDescription(e.target.value)}
//               placeholder="Description"
//               required
//             />
//             <button type="submit">Add Income</button>
//             <button type="button" onClick={toggleIncomeForm}>
//               Cancel
//             </button>
//           </form>
//         </div>
//       )}

//       <div className="transactions">
//         <h3>Past Transactions</h3>
//         {error && <p className="error">{error}</p>}
//         {transactions.length === 0 ? (
//           <p>No transactions yet.</p>
//         ) : (
//           <div>
//             <label htmlFor="categoryFilter">Filter by Category:</label>
//             <select
//               id="categoryFilter"
//               onChange={(e) => {
//                 const category = e.target.value;
//                 if (category) {
//                   setTransactions(transactions.filter((t) => t.category_name === category));
//                 } else {
//                   // Reset to all transactions if no filter
//                   setTransactions(transactions);
//                 }
//               }}
//             >
//               <option value="">All Categories</option>
//               {categories.map((category) => (
//                 <option key={category.category_id} value={category.name}>
//                   {category.name}
//                 </option>
//               ))}
//             </select>

//             <table>
//               <thead>
//                 <tr>
//                   <th>Date</th>
//                   <th>Amount</th>
//                   <th>Category</th>
//                   <th>Description</th>
//                 </tr>
//               </thead>
//               <tbody>
//                 {transactions.map((transaction, index) => (
//                   <tr key={index}>
//                     <td>{transaction.date}</td>
//                     <td>{transaction.amount}</td>
//                     <td>{transaction.category_name}</td>
//                     <td>{transaction.description}</td>
//                   </tr>
//                 ))}
//               </tbody>
//             </table>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// }
