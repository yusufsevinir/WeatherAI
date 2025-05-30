import React, { useEffect, useState } from 'react';
import { weatherService } from '../services/weatherService';

interface SampleQueriesProps {
  onSelect: (query: string) => void;
}

const SampleQueries: React.FC<SampleQueriesProps> = ({ onSelect }) => {
  const [queries, setQueries] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    weatherService.getSampleQueries()
      .then(setQueries)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="mt-4 text-cyan-700">Loading suggestions...</div>;
  if (error) return <div className="mt-4 text-red-600">{error}</div>;
  if (!queries.length) return null;

  // Limit to 6 queries
  const limitedQueries = queries.slice(0, 6);

  return (
    <div className="mt-4 overflow-x-auto">
      <div className="flex gap-3 w-max" style={{ minWidth: '360px' }}>
        <div className="grid grid-rows-3 grid-cols-2 gap-3">
          {limitedQueries.map((q, idx) => (
            <button
              key={idx}
              className="bg-cyan-100 hover:bg-cyan-200 text-cyan-900 px-4 py-2 rounded-lg shadow text-base transition border border-cyan-200 whitespace-nowrap"
              onClick={() => onSelect(q)}
              type="button"
            >
              {q}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SampleQueries; 