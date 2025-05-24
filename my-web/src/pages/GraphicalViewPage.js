import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { format, subDays, subMonths } from 'date-fns';
import './Graph.css';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#A28BFE', '#FE7B72', '#82CA9D', '#8884D8', '#FBAF00'];

const GraphicalViewPage = () => {
  const location = useLocation();
  const user = location.state?.user;
  const userId = user?.user_id || '';

  const [categoryExpenditure, setCategoryExpenditure] = useState([]);
  const [allTransactions, setAllTransactions] = useState([]);
  const [last7DaysTransactions, setLast7DaysTransactions] = useState([]);
  const [lastMonthTransactions, setLastMonthTransactions] = useState([]);
  const [budgetSummaryData, setBudgetSummaryData] = useState([]);
  const [balanceData, setBalanceData] = useState({ average_balance: 0, current_balance: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchGraphData = async () => {
      if (!userId) {
        setLoading(false);
        setError('User ID is missing!');
        return;
      }

      try {
        const [categoryRes, allTxnRes, budgetRes, balanceRes] = await Promise.all([
          axios.get(`http://localhost:5000/graphical/category-expenditure/${userId}`),
          axios.get(`http://localhost:5000/graphical/transactions/${userId}`),
          axios.get(`http://localhost:5000/budget-summary/${userId}`),
          axios.get(`http://localhost:5000/graphical/balance/${userId}`)
        ]);

        setCategoryExpenditure(categoryRes.data);
        setAllTransactions(allTxnRes.data);
        setBudgetSummaryData(budgetRes.data);
        setBalanceData(balanceRes.data);
      } catch (err) {
        console.error('Error fetching graphical data:', err);
        setError('Failed to fetch graphical data.');
      } finally {
        setLoading(false);
      }
    };

    if (userId) {
      fetchGraphData();
    }
  }, [userId]);

  useEffect(() => {
    if (allTransactions.length > 0) {
      const sevenDaysAgo = subDays(new Date(), 7);
      const oneMonthAgo = subMonths(new Date(), 1);

      const last7Days = allTransactions.filter(t => new Date(t.date) >= sevenDaysAgo);
      const lastMonth = allTransactions.filter(t => new Date(t.date) >= oneMonthAgo);

      setLast7DaysTransactions(last7Days);
      setLastMonthTransactions(lastMonth);
    }
  }, [allTransactions]);

  if (loading) return <div className="text-center mt-10 text-xl font-semibold">Loading Graphical Data...</div>;
  if (error) return <div className="text-center mt-10 text-red-500">{error}</div>;

  return (
    <div className="graphical-page">
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white p-8">
      <h1 className="text-4xl font-bold mb-8 text-center">Graphical Expenditure Analysis</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
        {/* Category-wise Expenditure (Pie Chart) */}
        {categoryExpenditure.length > 0 && (
          <div className="bg-gray-700 p-6 rounded-2xl shadow-lg">
            <h2 className="text-2xl font-semibold mb-4">Category Wise Expenditure</h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={categoryExpenditure}
                  dataKey="total_amount"
                  nameKey="category_name"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label
                >
                  {categoryExpenditure.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={value => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(value)} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Last 7 Days Bar Chart */}
        {last7DaysTransactions.length > 0 && (
          <div className="bg-gray-700 p-6 rounded-2xl shadow-lg">
            <h2 className="text-2xl font-semibold mb-4">Transactions Last 7 Days</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={last7DaysTransactions}>
                <XAxis dataKey="date" tickFormatter={date => format(new Date(date), 'dd MMM')} />
                <YAxis tickFormatter={v => `₹${v}`} />
                <Tooltip formatter={v => `₹${v}`} />
                <Legend />
                <Bar dataKey="amount" fill="#82CA9D" name="Amount" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Last Month Bar Chart */}
        {lastMonthTransactions.length > 0 && (
          <div className="bg-gray-700 p-6 rounded-2xl shadow-lg">
            <h2 className="text-2xl font-semibold mb-4">Transactions Last Month</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={lastMonthTransactions}>
                <XAxis dataKey="date" tickFormatter={date => format(new Date(date), 'dd MMM')} />
                <YAxis tickFormatter={v => `₹${v}`} />
                <Tooltip formatter={v => `₹${v}`} />
                <Legend />
                <Bar dataKey="amount" fill="#FFBB28" name="Amount" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Budget Summary Table */}
        {budgetSummaryData.length > 0 && (
          <div className="bg-gray-700 p-6 rounded-2xl shadow-lg col-span-1 md:col-span-2 lg:col-span-3">
            <h2 className="text-2xl font-semibold mb-4">Budget Summary</h2>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-600">
                <thead className="bg-gray-800">
                  <tr>
                    {['Budget Name', 'Category', 'Budgeted Amount', 'Total Spent', 'Remaining', 'Period'].map(header => (
                      <th key={header} className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                        {header}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="bg-gray-700 divide-y divide-gray-600">
                  {budgetSummaryData.map(budget => (
                    <tr key={budget.budget_name}>
                      <td className="px-6 py-4">{budget.budget_name}</td>
                      <td className="px-6 py-4">{budget.category_name}</td>
                      <td className="px-6 py-4 text-right">₹{budget.budget_amount}</td>
                      <td className="px-6 py-4 text-right">₹{budget.total_spent}</td>
                      <td className="px-6 py-4 text-right">₹{budget.remaining}</td>
                      <td className="px-6 py-4 text-center">
                        {format(new Date(budget.start_date), 'dd MMM')} - {format(new Date(budget.end_date), 'dd MMM')}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Balance Overview */}
        <div className="bg-gray-700 p-6 rounded-2xl shadow-lg">
          <h2 className="text-2xl font-semibold mb-4">Balance Overview</h2>
          <p className="text-lg">
            <span className="font-semibold">Average Balance:</span>{' '}
            ₹{balanceData.average_balance.toLocaleString('en-IN')}
          </p>
          <p className="text-lg">
            <span className="font-semibold">Current Balance:</span>{' '}
            ₹{balanceData.current_balance.toLocaleString('en-IN')}
          </p>
        </div>
      </div>
    </div>
    </div>
  );
};

export default GraphicalViewPage;

// import React, { useEffect, useState } from 'react';
// import axios from 'axios';
// import { useLocation } from 'react-router-dom';
// import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
// import { format, subDays, subMonths } from 'date-fns';
// import './Graph.css';

// const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#A28BFE', '#FE7B72', '#82CA9D', '#8884D8', '#FBAF00'];

// const GraphicalViewPage = () => {
//   const location = useLocation();
//   const user = location.state?.user; // Assuming user is passed in location.state
//   const userId = user?.user_id || ''; // Check if userId is available

//   const [categoryExpenditure, setCategoryExpenditure] = useState([]);
//   const [allTransactions, setAllTransactions] = useState([]);
//   const [last7DaysTransactions, setLast7DaysTransactions] = useState([]);
//   const [lastMonthTransactions, setLastMonthTransactions] = useState([]);
//   const [budgetSummaryData, setBudgetSummaryData] = useState([]);
//   const [balanceData, setBalanceData] = useState({ average_balance: 0, current_balance: 0 });
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState('');

//   useEffect(() => {
//     const fetchGraphData = async () => {
//       if (!userId) {
//         setLoading(false);
//         setError('User ID is missing!');
//         return;
//       }

//       try {
//         const categoryResponse = await axios.get(`http://localhost:5000/graphical/category-expenditure/${userId}`);
//         setCategoryExpenditure(categoryResponse.data);

//         const allTransactionsResponse = await axios.get(`http://localhost:5000/graphical/transactions/${userId}`);
//         setAllTransactions(allTransactionsResponse.data);

//         const budgetSummaryResponse = await axios.get(`http://localhost:5000/budget-summary/${userId}`);
//         setBudgetSummaryData(budgetSummaryResponse.data);

//         const balanceResponse = await axios.get(`http://localhost:5000/graphical/balance/${userId}`);
//         setBalanceData(balanceResponse.data);

//       } catch (err) {
//         console.error('Error fetching graphical data:', err);
//         setError('Failed to fetch graphical data.');
//       } finally {
//         setLoading(false);
//       }
//     };

//     if (userId) {
//       fetchGraphData();
//     }
//   }, [userId]);

//   useEffect(() => {
//     if (allTransactions && allTransactions.length > 0) {
//       const sevenDaysAgo = subDays(new Date(), 7);
//       const oneMonthAgo = subMonths(new Date(), 1);

//       const last7Days = allTransactions.filter(t => new Date(t.date) >= sevenDaysAgo);
//       setLast7DaysTransactions(last7Days);

//       const lastMonth = allTransactions.filter(t => new Date(t.date) >= oneMonthAgo);
//       setLastMonthTransactions(lastMonth);
//     }
//   }, [allTransactions]);

//   if (loading) {
//     return <div className="text-center mt-10 text-xl font-semibold">Loading Graphical Data...</div>;
//   }

//   if (error) {
//     return <div className="text-center mt-10 text-red-500">{error}</div>;
//   }

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white p-8">
//       <h1 className="text-4xl font-bold mb-8 text-center text-white">Graphical Expenditure Analysis</h1>

//       <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
//         {/* Category Wise Pie Chart */}
//         {categoryExpenditure && categoryExpenditure.length > 0 && (
//           <div className="bg-gray-700 p-6 rounded-2xl shadow-lg">
//             <h2 className="text-2xl font-semibold mb-4">Category Wise Expenditure</h2>
//             <ResponsiveContainer width="100%" height={300}>
//               <PieChart>
//                 <Pie
//                   data={categoryExpenditure}
//                   dataKey="total_amount"
//                   nameKey="category_name"
//                   cx="50%"
//                   cy="50%"
//                   outerRadius={100}
//                   fill="#8884d8"
//                   label
//                 >
//                   {categoryExpenditure.map((entry, index) => (
//                     <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
//                   ))}
//                 </Pie>
//                 <Tooltip formatter={(value) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(value)} />
//                 <Legend />
//               </PieChart>
//             </ResponsiveContainer>
//           </div>
//         )}

//         {/* Last 7 Days Transactions Bar Chart */}
//         {last7DaysTransactions && last7DaysTransactions.length > 0 && (
//           <div className="bg-gray-700 p-6 rounded-2xl shadow-lg">
//             <h2 className="text-2xl font-semibold mb-4">Transactions Last 7 Days</h2>
//             <ResponsiveContainer width="100%" height={300}>
//               <BarChart data={last7DaysTransactions}>
//                 <XAxis dataKey="date" tickFormatter={(date) => format(new Date(date), 'dd MMM')} />
//                 <YAxis tickFormatter={(value) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(value)} />
//                 <Tooltip formatter={(value) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(value)} />
//                 <Legend />
//                 <Bar dataKey="amount" fill="#82CA9D" name="Amount" />
//               </BarChart>
//             </ResponsiveContainer>
//           </div>
//         )}

//         {/* Last Month Transactions Bar Chart */}
//         {lastMonthTransactions && lastMonthTransactions.length > 0 && (
//           <div className="bg-gray-700 p-6 rounded-2xl shadow-lg">
//             <h2 className="text-2xl font-semibold mb-4">Transactions Last Month</h2>
//             <ResponsiveContainer width="100%" height={300}>
//               <BarChart data={lastMonthTransactions}>
//                 <XAxis dataKey="date" tickFormatter={(date) => format(new Date(date), 'dd MMM')} />
//                 <YAxis tickFormatter={(value) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(value)} />
//                 <Tooltip formatter={(value) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(value)} />
//                 <Legend />
//                 <Bar dataKey="amount" fill="#FFBB28" name="Amount" />
//               </BarChart>
//             </ResponsiveContainer>
//           </div>
//         )}

//         {/* Budget Summary */}
//         {budgetSummaryData && budgetSummaryData.length > 0 && (
//           <div className="bg-gray-700 p-6 rounded-2xl shadow-lg col-span-1 md:col-span-2 lg:col-span-3">
//             <h2 className="text-2xl font-semibold mb-4">Budget Summary</h2>
//             <div className="overflow-x-auto">
//               <table className="min-w-full divide-y divide-gray-600">
//                 <thead className="bg-gray-800">
//                   <tr>
//                     <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Budget Name</th>
//                     <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Category</th>
//                     <th className="px-6 py-3 text-right text-xs font-medium text-gray-300 uppercase tracking-wider">Budgeted Amount</th>
//                     <th className="px-6 py-3 text-right text-xs font-medium text-gray-300 uppercase tracking-wider">Total Spent</th>
//                     <th className="px-6 py-3 text-right text-xs font-medium text-gray-300 uppercase tracking-wider">Remaining</th>
//                     <th className="px-6 py-3 text-center text-xs font-medium text-gray-300 uppercase tracking-wider">Period</th>
//                   </tr>
//                 </thead>
//                 <tbody className="bg-gray-700 divide-y divide-gray-600">
//                   {budgetSummaryData.map(budget => (
//                     <tr key={budget.budget_name}>
//                       <td className="px-6 py-4 whitespace-nowrap">{budget.budget_name}</td>
//                       <td className="px-6 py-4 whitespace-nowrap">{budget.category_name}</td>
//                       <td className="px-6 py-4 whitespace-nowrap text-right">{new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(budget.budget_amount)}</td>
//                       <td className="px-6 py-4 whitespace-nowrap text-right">{new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(budget.total_spent)}</td>
//                       <td className="px-6 py-4 whitespace-nowrap text-right">{new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(budget.remaining)}</td>
//                       <td className="px-6 py-4 whitespace-nowrap text-center">{format(new Date(budget.start_date), 'dd MMM')} - {format(new Date(budget.end_date), 'dd MMM')}</td>
//                     </tr>
//                   ))}
//                 </tbody>
//               </table>
//             </div>
//           </div>
//         )}

//         {/* Balance Information */}
//         <div className="bg-gray-700 p-6 rounded-2xl shadow-lg">
//           <h2 className="text-2xl font-semibold mb-4">Balance Overview</h2>
//           <p className="text-lg">
//             <span className="font-semibold">Average Balance:</span> {new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(balanceData.average_balance)}
//           </p>
//           <p className="text-lg">
//             <span className="font-semibold">Current Balance:</span> {new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(balanceData.current_balance)}
//           </p>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default GraphicalViewPage;
// import React, { useEffect, useState } from 'react';
// import axios from 'axios';
// import { useLocation } from 'react-router-dom';
// import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

// const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#A28BFE', '#FE7B72', '#82CA9D', '#8884D8', '#FBAF00'];

// const GraphicalViewPage = () => {
//   const location = useLocation();
//   const user = location.state?.user || {};
//   const userId = user.id || '';

//   const [categoryData, setCategoryData] = useState([]);
//   const [budgetData, setBudgetData] = useState([]);
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     const fetchGraphData = async () => {
//       try {
//         const categoryResponse = await axios.get(`http://localhost:5000/graphical/category-expenditure/${userId}`);
//         const budgetResponse = await axios.get(`http://localhost:5000/graphical/budget-expenditure/${userId}`);

//         if (categoryResponse.data && Array.isArray(categoryResponse.data)) {
//           setCategoryData(categoryResponse.data);
//         }
//         if (budgetResponse.data && Array.isArray(budgetResponse.data)) {
//           setBudgetData(budgetResponse.data);
//         }

//         setLoading(false);
//       } catch (error) {
//         console.error('Error fetching graphical data:', error);
//         setLoading(false);
//       }
//     };

//     if (userId) {
//       fetchGraphData();
//     }
//   }, [userId]);

//   if (loading) {
//     return <div className="text-center mt-10 text-xl font-semibold">Loading Graphical Data...</div>;
//   }

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white p-8">
//       <h1 className="text-4xl font-bold mb-8 text-center text-white">Graphical Expenditure Analysis</h1>

//       <div className="grid grid-cols-1 md:grid-cols-2 gap-12">

//         {/* Category Wise Pie Chart */}
//         <div className="bg-gray-700 p-6 rounded-2xl shadow-lg">
//           <h2 className="text-2xl font-semibold mb-4">Category Wise Expenditure</h2>
//           <ResponsiveContainer width="100%" height={300}>
//             <PieChart>
//               <Pie
//                 data={categoryData}
//                 dataKey="total_amount"
//                 nameKey="category_name"
//                 cx="50%"
//                 cy="50%"
//                 outerRadius={100}
//                 fill="#8884d8"
//                 label
//               >
//                 {categoryData.map((entry, index) => (
//                   <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
//                 ))}
//               </Pie>
//               <Tooltip />
//               <Legend />
//             </PieChart>
//           </ResponsiveContainer>
//         </div>

//         {/* Budget Wise Bar Chart */}
//         <div className="bg-gray-700 p-6 rounded-2xl shadow-lg">
//           <h2 className="text-2xl font-semibold mb-4">Budget Wise Expenditure</h2>
//           <ResponsiveContainer width="100%" height={300}>
//             <BarChart data={budgetData}>
//               <XAxis dataKey="budget_name" />
//               <YAxis />
//               <Tooltip />
//               <Legend />
//               <Bar dataKey="total_spent" fill="#FF8042" name="Spent" />
//               <Bar dataKey="remaining_amount" fill="#00C49F" name="Remaining" />
//             </BarChart>
//           </ResponsiveContainer>
//         </div>

//       </div>
//     </div>
//   );
// };

// export default GraphicalViewPage;
