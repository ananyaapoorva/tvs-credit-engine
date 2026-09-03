const TransactionHistory = () => {
  const sampleTransactions = [
    { date: '2025-01-14', type: 'UPI', amount: 4500, category: 'Payment Received' },
    { date: '2025-01-13', type: 'UPI', amount: 2200, category: 'Purchase' },
    { date: '2025-01-12', type: 'Utility', amount: 1800, category: 'Electricity Bill' },
    { date: '2025-01-10', type: 'Telecom', amount: 349, category: 'Mobile Recharge' },
    { date: '2025-01-08', type: 'E-commerce', amount: 2499, category: 'Online Purchase' },
    { date: '2025-01-05', type: 'GST', amount: 37500, category: 'GST Filing' },
    { date: '2025-01-03', type: 'Mobility', amount: 1200, category: 'Fuel Expense' },
    { date: '2024-12-28', type: 'UPI', amount: 8000, category: 'Payment Received' },
  ];

  const typeColors = {
    UPI: 'var(--primary)',
    GST: 'var(--success)',
    Telecom: '#8b5cf6',
    Utility: 'var(--warning)',
    'E-commerce': '#ec4899',
    Mobility: '#06b6d4',
  };

  return (
    <div className="card animate-in animate-delay-4">
      <div className="card-header">
        <h3 className="card-title"> Sample Transaction History</h3>
      </div>
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
          <thead>
            <tr style={{ borderBottom: '2px solid var(--border)' }}>
              <th style={{ textAlign: 'left', padding: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Date</th>
              <th style={{ textAlign: 'left', padding: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Type</th>
              <th style={{ textAlign: 'left', padding: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Category</th>
              <th style={{ textAlign: 'right', padding: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Amount</th>
            </tr>
          </thead>
          <tbody>
            {sampleTransactions.map((tx, i) => (
              <tr key={i} style={{ borderBottom: '1px solid var(--border)' }}>
                <td style={{ padding: '0.65rem 0.75rem', color: 'var(--text-secondary)' }}>{tx.date}</td>
                <td style={{ padding: '0.65rem 0.75rem' }}>
                  <span style={{
                    display: 'inline-block',
                    padding: '0.15rem 0.5rem',
                    borderRadius: 'var(--radius-full)',
                    fontSize: '0.75rem',
                    fontWeight: 600,
                    background: `${typeColors[tx.type]}15`,
                    color: typeColors[tx.type],
                  }}>
                    {tx.type}
                  </span>
                </td>
                <td style={{ padding: '0.65rem 0.75rem' }}>{tx.category}</td>
                <td style={{ padding: '0.65rem 0.75rem', textAlign: 'right', fontFamily: 'var(--font-mono)', fontWeight: 600 }}>
                  ₹{tx.amount.toLocaleString('en-IN')}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TransactionHistory;
