// Hand-written mirrors of the backend Pydantic models — nothing infers across the HTTP
// boundary, so this file must change in the same edit as backend/models/*.

export type ProductType = "barang" | "jasa";
export type PaymentMethod = "cash" | "credit";
export type TxStatus = "completed" | "returned";
export type DebtStatus = "unpaid" | "paid";
export type UserRole = "admin" | "kasir";

export interface Product {
  id: string;
  type: ProductType;
  sku: string;
  name: string;
  brand: string;
  size: string;
  stock: number;
  cost_price: number;
  selling_price: number;
  service_fee: number;
}

export interface Customer {
  id: string;
  name: string;
  phone: string;
  address: string;
}

export interface Supplier {
  id: string;
  name: string;
  phone: string;
  address: string;
}

export interface TransactionDetail {
  id: string;
  transaction_id: string;
  product_id: string;
  product_name: string;
  product_type: ProductType;
  qty: number;
  price: number;
  cost_price: number;
  service_fee: number;
  subtotal: number;
}

export interface Transaction {
  id: string;
  invoice_number: string;
  date: string;
  date_key: string;
  customer_id: string | null;
  customer_name: string | null;
  payment_method: PaymentMethod;
  total_amount: number;
  barang_amount: number;
  jasa_amount: number;
  total_cost: number;
  service_fee: number;
  total_profit: number;
  status: TxStatus;
  due_date: string | null;
  details: TransactionDetail[];
}

export interface AccountsReceivable {
  id: string;
  transaction_id: string;
  invoice_number: string;
  customer_id: string;
  customer_name: string;
  amount: number;
  due_date: string;
  status: DebtStatus;
}

export interface AccountsPayable {
  id: string;
  supplier_id: string;
  supplier_name: string;
  invoice_number: string;
  amount: number;
  due_date: string;
  status: DebtStatus;
}

export interface Expense {
  id: string;
  date: string;
  amount: number;
  category: string;
  description: string;
}

export interface User {
  id: string;
  name: string;
  username: string;
  role: UserRole;
}

export interface DayRevenue {
  date_key: string;
  label: string;
  revenue: number;
  profit: number;
}

export interface DashboardStats {
  today: string;
  total_revenue: number;
  total_cost: number;
  gross_profit: number;
  jasa_amount: number;
  service_fee_total: number;
  expenses_total: number;
  net_profit: number;
  transaction_count: number;
  today_revenue: number;
  receivables_outstanding: number;
  receivables_overdue: number;
  payables_outstanding: number;
  payables_overdue: number;
  low_stock: Product[];
  revenue_by_day: DayRevenue[];
  overdue_receivables: AccountsReceivable[];
  overdue_payables: AccountsPayable[];
  recent_transactions: Transaction[];
}

export interface LaravelBundleFile {
  path: string;
  description: string;
  code: string;
}
