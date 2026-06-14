export const formatCurrency = (value) => {
  if (value === undefined || value === null) return '-';
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value);
};

export const formatPercentage = (value) => {
  if (value === undefined || value === null) return '-';
  return new Intl.NumberFormat('id-ID', {
    style: 'decimal',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value) + '%';
};

export const formatDate = (dateString) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('id-ID', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  }).format(date);
};

export const formatShortCurrency = (value) => {
  if (value === undefined || value === null) return '-';
  if (value >= 1000000) {
    return 'Rp ' + (value / 1000000).toFixed(1).replace('.', ',') + 'M';
  }
  if (value >= 1000) {
    return 'Rp ' + (value / 1000).toFixed(1).replace('.', ',') + 'K';
  }
  return 'Rp ' + value.toString().replace('.', ',');
};
