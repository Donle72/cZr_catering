import { useState, useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import { TrendingUp, TrendingDown, DollarSign, Calendar, Package, ChefHat } from 'lucide-react'
import CreateEventModal from '../components/events/CreateEventModal'
import CreateRecipeModal from '../components/recipes/CreateRecipeModal'
import CreateIngredientModal from '../components/ingredients/CreateIngredientModal'

const statusColors = {
    confirmed: 'bg-green-100 text-green-800',
    quoted: 'bg-yellow-100 text-yellow-800',
    prospect: 'bg-blue-100 text-blue-800',
}

const statusLabels = {
    confirmed: 'Confirmado',
    quoted: 'Cotizado',
    prospect: 'Prospecto',
}

export default function Dashboard() {
    const navigate = useNavigate()
    const [isEventModalOpen, setIsEventModalOpen] = useState(false)
    const [isRecipeModalOpen, setIsRecipeModalOpen] = useState(false)
    const [isIngredientModalOpen, setIsIngredientModalOpen] = useState(false)

    // Data Fetching
    const { data: eventsData } = useQuery({
        queryKey: ['dashboard_events'],
        queryFn: async () => {
            const res = await axios.get('/api/v1/events/?limit=5')
            return res.data
        }
    })

    const { data: statsData } = useQuery({
        queryKey: ['dashboard_stats'],
        queryFn: async () => {
            const res = await axios.get('/api/v1/stats/dashboard')
            return res.data
        }
    })

    // Computed Stats
    const stats = useMemo(() => [
        {
            name: 'Eventos del Mes',
            value: statsData?.events_month || 0,
            change: '-',
            changeType: 'neutral',
            icon: Calendar,
            color: 'from-blue-500 to-blue-600'
        },
        {
            name: 'Ingresos Estimados',
            value: new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS' }).format(statsData?.revenue_month || 0),
            change: '-',
            changeType: 'neutral',
            icon: DollarSign,
            color: 'from-green-500 to-green-600'
        },
        {
            name: 'Recetas Activas',
            value: statsData?.active_recipes || 0,
            change: '-',
            changeType: 'neutral',
            icon: ChefHat,
            color: 'from-purple-500 to-purple-600'
        },
        {
            name: 'Ingredientes',
            value: statsData?.total_ingredients || 0,
            change: '-',
            changeType: 'neutral',
            icon: Package,
            color: 'from-orange-500 to-orange-600'
        },
    ], [statsData])

    // Recent Events Mapping
    const recentEvents = eventsData?.items?.map(ev => ({
        id: ev.id,
        name: ev.name,
        date: new Date(ev.event_date).toLocaleDateString(),
        guests: ev.guest_count,
        status: ev.status
    })) || []

    return (
        <div className="space-y-6 animate-fade-in">
            {/* Welcome Section */}
            <div className="card bg-gradient-to-r from-primary-600 to-primary-700 text-white">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold mb-2">¡Bienvenido de vuelta! 👋</h1>
                        <p className="text-primary-100">
                            Aquí tienes un resumen de tu operación de catering
                        </p>
                    </div>
                    <div className="hidden md:block">
                        <div className="w-32 h-32 bg-white/10 rounded-full flex items-center justify-center backdrop-blur-sm">
                            <ChefHat className="w-16 h-16" />
                        </div>
                    </div>
                </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {stats.map((stat) => (
                    <div key={stat.name} className="card-hover group">
                        <div className="flex items-center justify-between mb-4">
                            <div className={`w-12 h-12 bg-gradient-to-br ${stat.color} rounded-xl flex items-center justify-center text-white shadow-lg group-hover:scale-110 transition-transform`}>
                                <stat.icon className="w-6 h-6" />
                            </div>
                            <div className={`flex items-center space-x-1 text-sm font-medium ${stat.changeType === 'positive' ? 'text-green-600' :
                                stat.changeType === 'negative' ? 'text-red-600' : 'text-gray-600'
                                }`}>
                                {stat.changeType === 'positive' && <TrendingUp className="w-4 h-4" />}
                                {stat.changeType === 'negative' && <TrendingDown className="w-4 h-4" />}
                                <span>{stat.change}</span>
                            </div>
                        </div>
                        <h3 className="text-2xl font-bold text-gray-900 mb-1">{stat.value}</h3>
                        <p className="text-sm text-gray-600">{stat.name}</p>
                    </div>
                ))}
            </div>

            {/* Recent Events */}
            <div className="card">
                <div className="flex items-center justify-between mb-6">
                    <h2 className="text-xl font-bold text-gray-900">Próximos Eventos</h2>
                    <button type="button" onClick={() => navigate('/events')} className="btn btn-primary text-sm">
                        Ver Todos
                    </button>
                </div>

                <div className="space-y-4">
                    {recentEvents.length > 0 ? (
                        recentEvents.map((event) => (
                            <div
                                key={event.id}
                                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer"
                            >
                                <div className="flex items-center space-x-4">
                                    <div className="w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg flex items-center justify-center text-white font-bold">
                                        {event.guests}
                                    </div>
                                    <div>
                                        <h3 className="font-semibold text-gray-900">{event.name}</h3>
                                        <p className="text-sm text-gray-600">{event.date}</p>
                                    </div>
                                </div>
                                <div className="flex items-center space-x-3">
                                    <span className="text-sm text-gray-600">{event.guests} invitados</span>
                                    <span className={`badge ${statusColors[event.status] || 'bg-gray-100'}`}>
                                        {statusLabels[event.status] || event.status}
                                    </span>
                                </div>
                            </div>
                        ))
                    ) : (
                        <p className="text-center text-gray-500 py-4">No hay eventos recientes.</p>
                    )}
                </div>
            </div>

            {/* Quick Actions */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <button type="button" onClick={() => setIsEventModalOpen(true)} className="card-hover text-left group">
                    <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center text-white mb-4 group-hover:scale-110 transition-transform">
                        <Calendar className="w-6 h-6" />
                    </div>
                    <h3 className="font-bold text-gray-900 mb-2">Nuevo Evento</h3>
                    <p className="text-sm text-gray-600">Crear una nueva cotización o evento</p>
                </button>

                <button type="button" onClick={() => setIsRecipeModalOpen(true)} className="card-hover text-left group">
                    <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center text-white mb-4 group-hover:scale-110 transition-transform">
                        <ChefHat className="w-6 h-6" />
                    </div>
                    <h3 className="font-bold text-gray-900 mb-2">Nueva Receta</h3>
                    <p className="text-sm text-gray-600">Agregar una receta al sistema</p>
                </button>

                <button type="button" onClick={() => setIsIngredientModalOpen(true)} className="card-hover text-left group">
                    <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl flex items-center justify-center text-white mb-4 group-hover:scale-110 transition-transform">
                        <Package className="w-6 h-6" />
                    </div>
                    <h3 className="font-bold text-gray-900 mb-2">Nuevo Ingrediente</h3>
                    <p className="text-sm text-gray-600">Registrar un nuevo ingrediente</p>
                </button>
            </div>

            <CreateEventModal
                isOpen={isEventModalOpen}
                onClose={() => setIsEventModalOpen(false)}
            />

            <CreateRecipeModal
                isOpen={isRecipeModalOpen}
                onClose={() => setIsRecipeModalOpen(false)}
            />

            <CreateIngredientModal
                isOpen={isIngredientModalOpen}
                onClose={() => setIsIngredientModalOpen(false)}
            />
        </div>
    )
}
