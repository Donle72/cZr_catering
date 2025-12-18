import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Plus, Search, Filter, TrendingUp, DollarSign, Edit, Trash2 } from 'lucide-react'
import axios from 'axios'
import CreateIngredientModal from '../components/ingredients/CreateIngredientModal'
import Pagination from '../components/ui/Pagination'

export default function Ingredients() {
    const queryClient = useQueryClient()
    const [searchTerm, setSearchTerm] = useState('')
    const [selectedCategory, setSelectedCategory] = useState('')
    const [editingIngredient, setEditingIngredient] = useState(null)
    const [page, setPage] = useState(1)
    const [limit] = useState(10)

    // Fetch ingredients
    const { data, isLoading, error } = useQuery({
        queryKey: ['ingredients', searchTerm, selectedCategory, page, limit],
        queryFn: async () => {
            const params = new URLSearchParams()
            if (searchTerm) params.append('search', searchTerm)
            if (selectedCategory) params.append('category', selectedCategory)
            params.append('skip', (page - 1) * limit)
            params.append('limit', limit)

            const response = await axios.get(`/api/v1/ingredients/?${params}`)
            return response.data
        },
        keepPreviousData: true
    })

    const { data: statsData } = useQuery({
        queryKey: ['dashboard_stats'],
        queryFn: async () => {
            const res = await axios.get('/api/v1/stats/dashboard')
            return res.data
        }
    })

    const totalIngredients = data?.total || 0
    const totalPages = Math.ceil(totalIngredients / limit)

    const deleteMutation = useMutation({
        mutationFn: async (id) => {
            await axios.delete(`/api/v1/ingredients/${id}`)
        },
        onSuccess: () => {
            queryClient.invalidateQueries(['ingredients'])
            queryClient.invalidateQueries(['ingredients_list'])
            alert('Ingrediente eliminado exitosamente')
        },
        onError: (error) => {
            if (error.response?.status === 409) {
                // Ingredient is in use
                const detail = error.response.data.detail
                const recipeList = detail.recipes_using?.join(', ') || 'recetas'
                const message = `❌ ${detail.message}\n\n` +
                    `📋 Recetas que lo usan:\n${recipeList}\n\n` +
                    `💡 ${detail.suggestion}`
                alert(message)
            } else {
                alert('Error al eliminar: ' + (error.response?.data?.detail || error.message))
            }
        }
    })

    const handleEdit = (ingredient) => {
        setEditingIngredient(ingredient)
        setIsModalOpen(true)
    }

    const handleDelete = (id) => {
        if (window.confirm('¿Estás seguro de eliminar este ingrediente?')) {
            deleteMutation.mutate(id)
        }
    }

    const handleCloseModal = () => {
        setIsModalOpen(false)
        setEditingIngredient(null)
    }

    const categories = ['Carnes', 'Vegetales', 'Lácteos', 'Granos', 'Especias', 'Bebidas']

    const [isModalOpen, setIsModalOpen] = useState(false)

    return (
        <div className="space-y-6 animate-fade-in">
            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">Ingredientes</h1>
                    <p className="text-gray-600">Gestiona tu inventario con control de rendimiento y costos</p>
                </div>
                <button
                    onClick={() => { setEditingIngredient(null); setIsModalOpen(true); }}
                    className="btn btn-primary flex items-center space-x-2"
                >
                    <Plus className="w-5 h-5" />
                    <span>Nuevo Ingrediente</span>
                </button>
            </div>

            {/* Modal */}
            <CreateIngredientModal
                isOpen={isModalOpen}
                onClose={handleCloseModal}
                ingredientToEdit={editingIngredient}
                onSuccess={(data) => {
                    handleCloseModal()
                    queryClient.invalidateQueries(['ingredients'])
                }}
            />

            {/* Filters */}
            <div className="card">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {/* Search */}
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                        <input
                            type="text"
                            placeholder="Buscar ingredientes..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="input pl-10"
                        />
                    </div>

                    {/* Category Filter */}
                    <div className="relative">
                        <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                        <select
                            value={selectedCategory}
                            onChange={(e) => setSelectedCategory(e.target.value)}
                            className="input pl-10"
                        >
                            <option value="">Todas las categorías</option>
                            {categories.map(cat => (
                                <option key={cat} value={cat}>{cat}</option>
                            ))}
                        </select>
                    </div>

                    {/* Bulk Price Update */}
                    <button className="btn btn-secondary flex items-center justify-center space-x-2">
                        <TrendingUp className="w-5 h-5" />
                        <span>Actualización Masiva</span>
                    </button>
                </div>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="card bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-blue-600 font-medium mb-1">Total Ingredientes</p>
                            <p className="text-3xl font-bold text-blue-900">{totalIngredients}</p>
                        </div>
                        <div className="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center">
                            <DollarSign className="w-6 h-6 text-white" />
                        </div>
                    </div>
                </div>

                <div className="card bg-gradient-to-br from-green-50 to-green-100 border-green-200">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-green-600 font-medium mb-1">Valor Inventario</p>
                            <p className="text-3xl font-bold text-green-900">
                                {new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS' }).format(statsData?.inventory_value || 0)}
                            </p>
                        </div>
                        <div className="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center">
                            <DollarSign className="w-6 h-6 text-white" />
                        </div>
                    </div>
                </div>

                <div className="card bg-gradient-to-br from-orange-50 to-orange-100 border-orange-200">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-orange-600 font-medium mb-1">Bajo Stock</p>
                            <p className="text-3xl font-bold text-orange-900">{statsData?.low_stock_count || 0}</p>
                        </div>
                        <div className="w-12 h-12 bg-orange-500 rounded-xl flex items-center justify-center">
                            <TrendingUp className="w-6 h-6 text-white" />
                        </div>
                    </div>
                </div>
            </div>

            {/* Ingredients Table */}
            <div className="card overflow-hidden p-0">
                {isLoading ? (
                    <div className="p-12 text-center">
                        <div className="inline-block w-8 h-8 border-4 border-primary-500 border-t-transparent rounded-full animate-spin"></div>
                        <p className="mt-4 text-gray-600">Cargando ingredientes...</p>
                    </div>
                ) : error ? (
                    <div className="p-12 text-center">
                        <p className="text-red-600">Error al cargar ingredientes</p>
                        <p className="text-sm text-gray-600 mt-2">Asegúrate de que el backend esté corriendo</p>
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead className="bg-gray-50 border-b border-gray-200">
                                <tr>
                                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                        Ingrediente
                                    </th>
                                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                        SKU
                                    </th>
                                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                        Categoría
                                    </th>
                                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                        Costo
                                    </th>
                                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                        Ratio Conversión
                                    </th>
                                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                        Rendimiento
                                    </th>
                                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                        Costo Real
                                    </th>
                                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                        Stock
                                    </th>
                                    <th className="px-6 py-4 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                        Acciones
                                    </th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-200">
                                {data?.items?.length > 0 ? (
                                    data.items.map((ingredient) => (
                                        <tr key={ingredient.id} className="hover:bg-gray-50 transition-colors">
                                            <td className="px-6 py-4">
                                                <div className="font-medium text-gray-900">{ingredient.name}</div>
                                                {ingredient.description && (
                                                    <div className="text-sm text-gray-500">{ingredient.description}</div>
                                                )}
                                            </td>
                                            <td className="px-6 py-4 text-sm text-gray-600">
                                                {ingredient.sku || '-'}
                                            </td>
                                            <td className="px-6 py-4">
                                                <span className="badge badge-info">{ingredient.category || 'Sin categoría'}</span>
                                            </td>
                                            <td className="px-6 py-4 text-sm font-medium text-gray-900">
                                                ${ingredient.current_cost.toFixed(2)}
                                            </td>
                                            <td className="px-6 py-4 text-sm text-gray-700">
                                                {ingredient.conversion_ratio} {ingredient.conversion_unit || ''}
                                            </td>
                                            <td className="px-6 py-4 text-sm font-medium text-gray-700">
                                                {(ingredient.yield_factor * 100).toFixed(0)}%
                                            </td>
                                            <td className="px-6 py-4 text-sm font-bold text-primary-600">
                                                ${ingredient.real_cost_per_usage_unit.toFixed(2)} x {ingredient.conversion_unit || 'unit'}
                                            </td>
                                            <td className="px-6 py-4 text-sm font-medium text-gray-900">
                                                {ingredient.stock_quantity || 0} {ingredient.purchase_unit?.abbreviation || ''}
                                            </td>
                                            <td className="px-6 py-4 text-right">
                                                <div className="flex items-center justify-end space-x-2">
                                                    <button
                                                        onClick={() => handleEdit(ingredient)}
                                                        className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                                                        title="Editar"
                                                    >
                                                        <Edit className="w-4 h-4" />
                                                    </button>
                                                    <button
                                                        onClick={() => handleDelete(ingredient.id)}
                                                        className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                                                        title="Eliminar"
                                                    >
                                                        <Trash2 className="w-4 h-4" />
                                                    </button>
                                                </div>
                                            </td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan="8" className="px-6 py-12 text-center text-gray-500">
                                            No hay ingredientes registrados. ¡Crea el primero!
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>

            <Pagination
                currentPage={page}
                totalPages={totalPages}
                onPageChange={setPage}
                hasNext={page < totalPages}
                hasPrev={page > 1}
            />
        </div>
    )
}
