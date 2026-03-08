type CardProps = {
  message: string
  description: string
}

const Card = ({ message, description }: CardProps) => {
  return (
    <div className="bg-white shadow-md rounded-xl p-6 border">
      <h3 className="text-lg font-semibold text-gray-800 mb-2">
        {message}
      </h3>
      <p className="text-gray-600">{description}</p>
    </div>
  )
}

export default Card