import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Plus, Calendar, Users, DollarSign, ArrowRight, Edit, Trash2 } from 'lucide-react'
import axios from 'axios'
import CreateEventModal from '../components/events/CreateEventModal'
import { Link } from 'react-router-dom'
import FloatingActionButton from '../components/ui/FloatingActionButton'
import Pagination from '../components/ui/Pagination'

export default function Events() {
    const queryClient = useQueryClient()
    const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
    const [editingEvent, setEditingEvent] = useState(null)
    const [page, setPage] = useState(1)
    const [limit] = useState(10)

    // Fetch Events with Pagination
    const { data, isLoading, error } = useQuery({
        queryKey: ['events', page, limit],
        queryFn: async () => {
            const res = await axios.get(`/api/v1/events/?skip=${(page - 1) * limit}&limit=${limit}`)
            return res.data
        },
        keepPreviousData: true
    })

    const events = data?.items || []
    const totalEvents = data?.total || 0
    const totalPages = Math.ceil(totalEvents / limit)

    const deleteMutation = useMutation({
        mutationFn: async (id) => {
            await axios.delete(`/api/v1/events/${id}`)
        },
        onSuccess: () => {
            queryClient.invalidateQueries(['events'])
        },
        onError: (error) => {
            alert('Error al eliminar evento: ' + (error.response?.data?.detail || error.message))
        }
    })

    const handleEdit = (event) => {
        setEditingEvent(event)
        setIsCreateModalOpen(true)
    }

    const handleDelete = (id) => {
        if (window.confirm('¿Estás seguro de eliminar este evento?')) {
            deleteMutation.mutate(id)
        }
    }

    const handleCloseModal = () => {
        setIsCreateModalOpen(false)
        setEditingEvent(null)
    }

    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('es-AR', {
            style: 'currency',
            currency: 'ARS',
            maximumFractionDigits: 0
        }).format(amount || 0)
    }

    // Calculate Summary Stats (Note: This only calculates for current page in this architecture, typically stats endpoint is separate)
    // For now, we use the returned totals if available in metadata, or summing the current page is acceptable for "Revenue" until a dedicated stats endpoint exists.
    const stats = {
        totalEvents: totalEvents, // From backend count
        totalRevenue: events.reduce((acc, ev) => acc + (ev.total_revenue || 0), 0), // Current Page Revenue
        totalGuests: events.reduce((acc, ev) => acc + (ev.guest_count || 0), 0) // Current Page Guests
    }


    if (isLoading) return <div className="p-8 text-center text-gray-500">Cargando eventos...</div>
    if (error) return <div className="p-8 text-center text-red-500">Error al cargar eventos</div>

    return (
        <div className="space-y-6 animate-fade-in pb-20">
            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">Eventos</h1>
                    <p className="text-gray-600">Gestiona tus eventos, cotizaciones y fechas.</p>
                </div>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="card border-l-4 border-l-blue-500">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-gray-500 font-medium mb-1">Total Eventos</p>
                            <p className="text-3xl font-bold text-gray-900">{stats.totalEvents}</p>
                        </div>
                        <div className="p-3 bg-blue-50 rounded-lg">
                            <Calendar className="w-6 h-6 text-blue-600" />
                        </div>
                    </div>
                </div>

                <div className="card border-l-4 border-l-green-500">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-gray-500 font-medium mb-1">Ingresos (Pág)</p>
                            <p className="text-3xl font-bold text-gray-900">{formatCurrency(stats.totalRevenue)}</p>
                        </div>
                        <div className="p-3 bg-green-50 rounded-lg">
                            <DollarSign className="w-6 h-6 text-green-600" />
                        </div>
                    </div>
                </div>

                <div className="card border-l-4 border-l-purple-500">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-gray-500 font-medium mb-1">Invitados (Pág)</p>
                            <p className="text-3xl font-bold text-gray-900">{stats.totalGuests}</p>
                        </div>
                        <div className="p-3 bg-purple-50 rounded-lg">
                            <Users className="w-6 h-6 text-purple-600" />
                        </div>
                    </div>
                </div>
            </div>

            {/* Event List */}
            <div className="card">
                <h2 className="text-xl font-bold text-gray-900 mb-6 px-2">Próximos Eventos</h2>

                {events.length === 0 ? (
                    <div className="text-center py-12 bg-gray-50 rounded-lg border border-dashed border-gray-200">
                        <Calendar className="w-12 h-12 text-gray-300 mx-auto mb-3" />
                        <p className="text-gray-500 mb-4">No tienes eventos registrados aún.</p>
                        <button
                            onClick={() => { setEditingEvent(null); setIsCreateModalOpen(true); }}
                            className="text-primary font-medium hover:underline"
                        >
                            Crear mi primer evento
                        </button>
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="border-b border-gray-100 text-sm">
                                    <th className="text-left py-3 px-4 text-gray-500 font-medium">Evento / Cliente</th>
                                    <th className="text-left py-3 px-4 text-gray-500 font-medium">Fecha</th>
                                    <th className="text-center py-3 px-4 text-gray-500 font-medium">Pax</th>
                                    <th className="text-right py-3 px-4 text-gray-500 font-medium">Estado</th>
                                    <th className="text-right py-3 px-4 text-gray-500 font-medium">Acción</th>
                                </tr>
                            </thead>
                            <tbody>
                                {events.map(event => (
                                    <tr key={event.id} className="border-b border-gray-50 hover:bg-gray-50 text-sm transition-colors">
                                        <td className="py-4 px-4">
                                            <div className="font-bold text-gray-900">{event.name}</div>
                                            <div className="text-xs text-gray-500">{event.client_name}</div>
                                        </td>
                                        <td className="py-4 px-4 text-gray-700">
                                            {new Date(event.event_date).toLocaleDateString()}
                                        </td>
                                        <td className="py-4 px-4 text-center text-gray-700">
                                            {event.guest_count}
                                        </td>
                                        <td className="py-4 px-4 text-right">
                                            <span className={`px-3 py-1 rounded-full text-xs font-medium ${event.status === 'confirmed' ? 'bg-green-100 text-green-700' :
                                                event.status === 'completed' ? 'bg-gray-100 text-gray-700' :
                                                    'bg-amber-100 text-amber-700'
                                                }`}>
                                                {event.status === 'confirmed' ? 'Confirmado' :
                                                    event.status === 'completed' ? 'Finalizado' : 'Borrador'}
                                            </span>
                                        </td>
                                        <td className="py-4 px-4 text-right">
                                            <div className="flex items-center justify-end space-x-2">
                                                <Link
                                                    to={`/events/${event.id}`}
                                                    onClick={(e) => e.stopPropagation()}
                                                    className="p-2 text-gray-400 hover:text-primary transition-colors"
                                                    title="Ver Detalles"
                                                >
                                                    <ArrowRight className="w-4 h-4" />
                                                </Link>
                                                <button
                                                    onClick={(e) => { e.stopPropagation(); handleEdit(event); }}
                                                    className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                                                    title="Editar"
                                                >
                                                    <Edit className="w-4 h-4" />
                                                </button>
                                                <button
                                                    onClick={(e) => { e.stopPropagation(); handleDelete(event.id); }}
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

                <Pagination
                    currentPage={page}
                    totalPages={totalPages}
                    onPageChange={setPage}
                    hasNext={page < totalPages}
                    hasPrev={page > 1}
                />
            </div>

            <FloatingActionButton
                onClick={() => { setEditingEvent(null); setIsCreateModalOpen(true); }}
                label="Nuevo Evento"
            />

            <CreateEventModal
                isOpen={isCreateModalOpen}
                onClose={handleCloseModal}
                eventToEdit={editingEvent}
            />
        </div>
    )
}
