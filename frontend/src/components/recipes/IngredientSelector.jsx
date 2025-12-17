import { useQuery } from '@tantml/react-query'
import axios from 'axios'
import { Search } from 'lucide-react'
import { useState } from 'react'
import PropTypes from 'prop-types'

export default function IngredientSelector({ value, onChange, error }) {
    const [searchTerm, setSearchTerm] = useState('')

    // Fetch all ingredients
    const { data: ingredientsData, isLoading } = useQuery({
        queryKey: ['ingredients'],
        queryFn: async () => {
            const response = await axios.get('/api/v1/ingredients/?limit=1000')
            return response.data
        }
    })

    const ingredients = ingredientsData?.items || []

    // Filter ingredients based on search
    const filteredIngredients = ingredients.filter(ing =>
        ing.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (ing.sku && ing.sku.toLowerCase().includes(searchTerm.toLowerCase()))
    )

    return (
        <div className="w-full space-y-2">
            {/* Search input */}
            <div className="relative">
                <input
                    type="text"
                    className="input pl-10 w-full"
                    placeholder="Buscar ingrediente..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
                <Search className="w-5 h-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
            </div>

            {/* Select dropdown */}
            <select
                className={`input w-full ${error ? 'border-red-500' : ''}`}
                value={value || ''}
                onChange={(e) => onChange(e.target.value)}
            >
                <option value="">Seleccionar ingrediente...</option>
                {isLoading ? (
                    <option disabled>Cargando ingredientes...</option>
                ) : filteredIngredients.length === 0 ? (
                    <option disabled>No se encontraron ingredientes</option>
                ) : (
                    filteredIngredients.map(ing => (
                        <option key={ing.id} value={ing.id}>
                            {ing.name} {ing.sku ? `(${ing.sku})` : ''} - ${ing.current_cost?.toFixed(2) || '0.00'}
                        </option>
                    ))
                )}
            </select>

            {error && (
                <p className="text-sm text-red-500">{error.message}</p>
            )}
        </div>
    )
}

IngredientSelector.propTypes = {
    value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    onChange: PropTypes.func.isRequired,
    error: PropTypes.object
}
