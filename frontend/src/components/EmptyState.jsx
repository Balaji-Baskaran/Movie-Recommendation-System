import React from 'react';
import { Film, AlertTriangle, AlertCircle, RefreshCw } from 'lucide-react';

export default function EmptyState({
  type = 'empty',
  title = 'No movies found',
  description = 'Try adjusting your search or filters to see recommendations.',
  onAction,
  actionLabel = 'Try Again',
}) {
  const getIcon = () => {
    switch (type) {
      case 'error':
        return <AlertCircle size={32} color="#ef4444" />;
      case 'warning':
        return <AlertTriangle size={32} color="#fbbf24" />;
      default:
        return <Film size={32} color="var(--accent)" />;
    }
  };

  return (
    <div className="empty-state">
      <div className="empty-state-icon">{getIcon()}</div>
      <h3>{title}</h3>
      <p>{description}</p>
      {onAction && (
        <button
          type="button"
          className="btn-primary"
          style={{ marginTop: '1.25rem' }}
          onClick={onAction}
        >
          <RefreshCw size={15} />
          <span>{actionLabel}</span>
        </button>
      )}
    </div>
  );
}
