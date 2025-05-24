export interface User {
    user_id: string;
    username: string;
    email: string;
  }
  
  export interface Transaction {
    amount: number;
    category_name?: string;
    source?: string;
    description: string;
    date: string;
    type: 'income' | 'expense';
  }
  
  export interface Category {
    category_id: number;
    name: string;
  }