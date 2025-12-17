import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Plus, Package, DollarSign, Wrench, Edit, Trash2, Filter } from 'lucide-react'
import axios from 'axios'
import CreateAssetModal from '../components/assets/CreateAssetModal'

export default function Assets() {
    const queryClient = useQueryClient()
    const [isModalOpen, setIsModalOpen] = useState(false)
    const [editingAsset, setEditingAsset] = useState(null)
    const [categoryFilter, setCategoryFilter] = useState('')

    // Fetch assets
    const { data: assets, isLoading, error } = useQuery({
        queryKey: ['assets', categoryFilter],
        queryFn: async () => {
            const params = new URLSearchParams()
            if (categoryFilter) params.append('category', categoryFilter)
            const response = await axios.get(`/api/v1/assets/?${params}`)
            return response.data
        }
    })

    const deleteMutation = useMutation({
        mutationFn: async (id) => {
            await axios.delete(`/api/v1/assets/${id}`)
        },
        onSuccess: () => {
            queryClient.invalidateQueries(['assets'])
        },
        onError: (error) => {
            alert('Error al eliminar: ' + (error.response?.data?.detail || error.message))
        }
    })

    const handleEdit = (asset) => {
        setEditingAsset(asset)
        setIsModalOpen(true)
    }

    const handleDelete = (id) => {
        if (window.confirm('¿Estás seguro de eliminar este activo?')) {
            deleteMutation.mutate(id)
        }
    }

    const handleCloseModal = () => {
        setIsModalOpen(false)
        setEditingAsset(null)
    }

    // Calculate stats
    const stats = assets ? {
        total: assets.length,
        totalValue: assets.reduce((acc, asset) => acc + (asset.purchase_price || 0) * (asset.total_quantity || 0), 0),
        available: assets.filter(a => a.state === 'available').length,
        maintenance: assets.filter(a => a.state === 'maintenance').length
    } : { total: 0, totalValue: 0, available: 0, maintenance: 0 }

    // Get unique categories
    const categories = assets ? [...new Set(assets.map(a => a.category).filter(Boolean))] : []

    const getStateColor = (state) => {
        switch (state) {
            case 'available': return 'bg-green-100 text-green-700'
            case 'maintenance': return 'bg-yellow-100 text-yellow-700'
            case 'broken': return 'bg-red-100 text-red-700'
            case 'lost': return 'bg-gray-100 text-gray-700'
            default: return 'bg-gray-100 text-gray-700'
        }
    }

    const getStateLabel = (state) => {
        switch (state) {
            case 'available': return 'Disponible'
            case 'maintenance': return 'Mantenimiento'
            case 'broken': return 'Roto'
            case 'lost': return 'Perdido'
            default: return state
        }
    }

    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('es-AR', {
            style: 'currency',
            currency: 'ARS',
            maximumFractionDigits: 0
        }).format(amount || 0)
    }

    return (
        <div className="space-y-6 animate-fade-in">
            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">Activos</h1>
                    <p className="text-gray-600">Gestiona tu inventario de equipamiento y mobiliario</p>
                </div>
                <button
                    type="button"
                    onClick={() => { setEditingAsset(null); setIsModalOpen(true); }}
                    className="btn btn-primary flex items-center space-x-2"
                >
                    <Plus className="w-5 h-5" />
                    <span>Nuevo Activo</span>
                </button>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="card bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-blue-600 font-medium mb-1">Total Activos</p>
                            <p className="text-3xl font-bold text-blue-900">{stats.total}</p>
                        </div>
                        <div className="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center">
                            <Package className="w-6 h-6 text-white" />
                        </div>
                    </div>
                </div>

                <div className="card bg-gradient-to-br from-green-50 to-green-100 border-green-200">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-green-600 font-medium mb-1">Disponibles</p>
                            <p className="text-3xl font-bold text-green-900">{stats.available}</p>
                        </div>
                        <div className="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center">
                            <Package className="w-6 h-6 text-white" />
                        </div>
                    </div>
                </div>

                <div className="card bg-gradient-to-br from-yellow-50 to-yellow-100 border-yellow-200">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-yellow-600 font-medium mb-1">Mantenimiento</p>
                            <p className="text-3xl font-bold text-yellow-900">{stats.maintenance}</p>
                        </div>
                        <div className="w-12 h-12 bg-yellow-500 rounded-xl flex items-center justify-center">
                            <Wrench className="w-6 h-6 text-white" />
                        </div>
                    </div>
                </div>

                <div className="card bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-purple-600 font-medium mb-1">Valor Total</p>
                            <p className="text-2xl font-bold text-purple-900">{formatCurrency(stats.totalValue)}</p>
                        </div>
                        <div className="w-12 h-12 bg-purple-500 rounded-xl flex items-center justify-center">
                            <DollarSign className="w-6 h-6 text-white" />
                        </div>
                    </div>
                </div>
            </div>

            {/* Filters */}
            <div className="card">
                <div className="flex items-center gap-4">
                    <Filter className="w-5 h-5 text-gray-400" />
                    <select
                        value={categoryFilter}
                        onChange={(e) => setCategoryFilter(e.target.value)}
                        className="input flex-1"
                    >
                        <option value="">Todas las categorías</option>
                        {categories.map(cat => (
                            <option key={cat} value={cat}>{cat}</option>
                        ))}
                    </select>
                </div>
            </div>

            {/* Assets List */}
            <div className="card overflow-hidden p-0">
                {isLoading ? (
                    <div className="p-12 text-center">
                        <div className="inline-block w-8 h-8 border-4 border-primary-500 border-t-transparent rounded-full animate-spin"></div>
                        <p className="mt-4 text-gray-600">Cargando activos...</p>
                    </div>
                ) : error ? (
                    <div className="p-12 text-center text-red-500">
                        Error al cargar activos
                    </div>
                ) : assets?.length === 0 ? (
                    <div className="p-12 text-center text-gray-500">
                        <Package className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                        <p className="text-lg font-medium mb-2">No hay activos registrados</p>
                        <p className="text-sm mb-4">Comienza agregando tu primer activo</p>
                        <button
                            onClick={() => { setEditingAsset(null); setIsModalOpen(true); }}
                            className="btn btn-primary"
                        >
                            Crear Activo
                        </button>
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead className="bg-gray-50 border-b border-gray-200">
                                <tr>
                                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Activo</th>
                                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Categoría</th>
                                    <th className="px-6 py-4 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider">Cantidad</th>
                                    <th className="px-6 py-4 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">Precio Unit.</th>
                                    <th className="px-6 py-4 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider">Estado</th>
                                    <th className="px-6 py-4 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">Acciones</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-200">
                                {assets.map((asset) => (
                                    <tr key={asset.id} className="hover:bg-gray-50 transition-colors">
                                        <td className="px-6 py-4">
                                            <div className="font-medium text-gray-900">{asset.name}</div>
                                            {asset.description && (
                                                <div className="text-xs text-gray-500 mt-1">{asset.description}</div>
                                            )}
                                            {asset.location && (
                                                <div className="text-xs text-gray-400 mt-1">📍 {asset.location}</div>
                                            )}
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs font-medium">
                                                {asset.category || 'Sin categoría'}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 text-center">
                                            <span className="text-lg font-bold text-gray-900">{asset.total_quantity}</span>
                                        </td>
                                        <td className="px-6 py-4 text-right text-gray-700">
                                            {formatCurrency(asset.purchase_price)}
                                        </td>
                                        <td className="px-6 py-4 text-center">
                                            <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStateColor(asset.state)}`}>
                                                {getStateLabel(asset.state)}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 text-right">
                                            <div className="flex items-center justify-end space-x-2">
                                                <button
                                                    onClick={() => handleEdit(asset)}
                                                    className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                                                    title="Editar"
                                                >
                                                    <Edit className="w-4 h-4" />
                                                </button>
                                                <button
                                                    onClick={() => handleDelete(asset.id)}
                                                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                                                    title="Eliminar"
                                                >
                                                    <Trash2 className="w-4 h-4" />
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>

            <CreateAssetModal
                isOpen={isModalOpen}
                onClose={handleCloseModal}
                assetToEdit={editingAsset}
            />
        </div>
    )
}
