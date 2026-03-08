type ResultCardProps = {
  quote: string;
  flag: string;
  solution: string;
};

const ResultCard = ({ quote, flag, solution }: ResultCardProps) => {
  return (
    <div className="bg-white shadow-md rounded-xl p-6 border">
      <h3 className="text-lg font-semibold text-gray-800 mb-2">Flag</h3>
      <p className="text-gray-600 mb-4">{flag}</p>

      <h3 className="text-lg font-semibold text-gray-800 mb-2">Solution</h3>
      <p className="text-gray-600 mb-4">{solution}</p>

      {quote && (
        <>
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Quote</h3>
          <p className="text-gray-600">{quote}</p>
        </>
      )}
    </div>
  );
};

export default ResultCard;