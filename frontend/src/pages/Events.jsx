import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Plus, Calendar, Users, DollarSign, ArrowRight } from 'lucide-react'
import axios from 'axios'
import CreateEventModal from '../components/events/CreateEventModal'
import { Link } from 'react-router-dom'

export default function Events() {
    const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)

    // Fetch Events
    const { data: events, isLoading, error } = useQuery({
        queryKey: ['events'],
        queryFn: async () => {
            const res = await axios.get('/api/v1/events/')
            return res.data
        }
    })

    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('es-AR', {
            style: 'currency',
            currency: 'ARS',
            maximumFractionDigits: 0
        }).format(amount || 0)
    }

    // Calculate Summary Stats
    const stats = events ? {
        totalEvents: events.length,
        totalRevenue: events.reduce((acc, ev) => acc + (ev.total_revenue || 0), 0),
        totalGuests: events.reduce((acc, ev) => acc + (ev.guest_count || 0), 0)
    } : { totalEvents: 0, totalRevenue: 0, totalGuests: 0 }


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
                <button
                    onClick={() => setIsCreateModalOpen(true)}
                    className="btn btn-primary flex items-center space-x-2"
                >
                    <Plus className="w-5 h-5" />
                    <span>Nuevo Evento</span>
                </button>
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
                            <p className="text-sm text-gray-500 font-medium mb-1">Ingresos Estimados</p>
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
                            <p className="text-sm text-gray-500 font-medium mb-1">Total Invitados</p>
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
                            onClick={() => setIsCreateModalOpen(true)}
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
                                            <Link
                                                // TODO: Create Event Detail Page
                                                to={`#`}
                                                className="inline-flex items-center text-sm font-medium text-primary hover:text-primary-700"
                                            >
                                                Ver Detalles
                                                <ArrowRight className="w-4 h-4 ml-1" />
                                            </Link>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>

            <CreateEventModal
                isOpen={isCreateModalOpen}
                onClose={() => setIsCreateModalOpen(false)}
            />
        </div>
    )
}
