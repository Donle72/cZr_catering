import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { ArrowLeft, Calendar, Users, DollarSign, MapPin, Mail, Phone } from 'lucide-react';

export default function EventDetail() {
    const { id } = useParams();
    const navigate = useNavigate();

    const { data: event, isLoading, error } = useQuery({
        queryKey: ['event', id],
        queryFn: async () => {
            const response = await axios.get(`/api/v1/events/${id}`);
            return response.data;
        }
    });

    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('es-AR', {
            style: 'currency',
            currency: 'ARS',
            maximumFractionDigits: 0
        }).format(amount || 0);
    };

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('es-AR', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    };

    if (isLoading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
                    <p className="text-gray-600">Cargando evento...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="p-8">
                <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
                    Error al cargar el evento: {error.response?.data?.detail || error.message}
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6 animate-fade-in">
            {/* Header */}
            <div className="flex items-center gap-4">
                <button
                    onClick={() => navigate('/events')}
                    className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                >
                    <ArrowLeft className="w-5 h-5" />
                </button>
                <div>
                    <h1 className="text-3xl font-bold text-gray-900">{event.name}</h1>
                    <p className="text-gray-600">{event.event_number}</p>
                </div>
            </div>

            {/* Status Badge */}
            <div>
                <span className={`px-4 py-2 rounded-full text-sm font-medium ${event.status === 'confirmed' ? 'bg-green-100 text-green-700' :
                        event.status === 'completed' ? 'bg-gray-100 text-gray-700' :
                            'bg-amber-100 text-amber-700'
                    }`}>
                    {event.status === 'confirmed' ? 'Confirmado' :
                        event.status === 'completed' ? 'Finalizado' : 'Borrador'}
                </span>
            </div>

            {/* Main Info Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="card border-l-4 border-l-blue-500">
                    <div className="flex items-center gap-3">
                        <div className="p-3 bg-blue-50 rounded-lg">
                            <Calendar className="w-6 h-6 text-blue-600" />
                        </div>
                        <div>
                            <p className="text-sm text-gray-500">Fecha</p>
                            <p className="font-bold text-gray-900">{formatDate(event.event_date)}</p>
                            {event.event_time && <p className="text-sm text-gray-600">{event.event_time}</p>}
                        </div>
                    </div>
                </div>

                <div className="card border-l-4 border-l-purple-500">
                    <div className="flex items-center gap-3">
                        <div className="p-3 bg-purple-50 rounded-lg">
                            <Users className="w-6 h-6 text-purple-600" />
                        </div>
                        <div>
                            <p className="text-sm text-gray-500">Invitados</p>
                            <p className="font-bold text-gray-900">{event.guest_count} pax</p>
                        </div>
                    </div>
                </div>

                <div className="card border-l-4 border-l-green-500">
                    <div className="flex items-center gap-3">
                        <div className="p-3 bg-green-50 rounded-lg">
                            <DollarSign className="w-6 h-6 text-green-600" />
                        </div>
                        <div>
                            <p className="text-sm text-gray-500">Ingresos</p>
                            <p className="font-bold text-gray-900">{formatCurrency(event.total_revenue || 0)}</p>
                        </div>
                    </div>
                </div>

                <div className="card border-l-4 border-l-orange-500">
                    <div className="flex items-center gap-3">
                        <div className="p-3 bg-orange-50 rounded-lg">
                            <DollarSign className="w-6 h-6 text-orange-600" />
                        </div>
                        <div>
                            <p className="text-sm text-gray-500">Margen</p>
                            <p className="font-bold text-gray-900">
                                {((event.margin || 0) * 100).toFixed(1)}%
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Client Info */}
            <div className="card">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Información del Cliente</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <p className="text-sm text-gray-500 mb-1">Nombre</p>
                        <p className="font-medium text-gray-900">{event.client_name}</p>
                    </div>
                    {event.client_email && (
                        <div className="flex items-center gap-2">
                            <Mail className="w-4 h-4 text-gray-400" />
                            <a href={`mailto:${event.client_email}`} className="text-primary hover:underline">
                                {event.client_email}
                            </a>
                        </div>
                    )}
                    {event.client_phone && (
                        <div className="flex items-center gap-2">
                            <Phone className="w-4 h-4 text-gray-400" />
                            <a href={`tel:${event.client_phone}`} className="text-primary hover:underline">
                                {event.client_phone}
                            </a>
                        </div>
                    )}
                </div>
            </div>

            {/* Venue Info */}
            {event.venue_name && (
                <div className="card">
                    <h2 className="text-xl font-bold text-gray-900 mb-4">Lugar del Evento</h2>
                    <div className="flex items-start gap-3">
                        <MapPin className="w-5 h-5 text-gray-400 mt-1" />
                        <div>
                            <p className="font-medium text-gray-900">{event.venue_name}</p>
                            {event.venue_address && (
                                <p className="text-gray-600">{event.venue_address}</p>
                            )}
                        </div>
                    </div>
                </div>
            )}

            {/* Orders */}
            {event.orders && event.orders.length > 0 && (
                <div className="card">
                    <h2 className="text-xl font-bold text-gray-900 mb-4">Pedidos</h2>
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="border-b border-gray-100 text-sm">
                                    <th className="text-left py-3 px-4 text-gray-500 font-medium">Receta</th>
                                    <th className="text-center py-3 px-4 text-gray-500 font-medium">Cantidad</th>
                                    <th className="text-right py-3 px-4 text-gray-500 font-medium">Precio Unit.</th>
                                    <th className="text-right py-3 px-4 text-gray-500 font-medium">Total</th>
                                </tr>
                            </thead>
                            <tbody>
                                {event.orders.map((order, index) => (
                                    <tr key={index} className="border-b border-gray-50 text-sm">
                                        <td className="py-3 px-4 font-medium text-gray-900">
                                            {order.recipe?.name || 'Receta eliminada'}
                                        </td>
                                        <td className="py-3 px-4 text-center text-gray-700">
                                            {order.quantity}
                                        </td>
                                        <td className="py-3 px-4 text-right text-gray-700">
                                            {formatCurrency(order.unit_price_frozen)}
                                        </td>
                                        <td className="py-3 px-4 text-right font-bold text-gray-900">
                                            {formatCurrency(order.unit_price_frozen * order.quantity)}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}

            {/* Description */}
            {event.description && (
                <div className="card">
                    <h2 className="text-xl font-bold text-gray-900 mb-4">Descripción</h2>
                    <p className="text-gray-700 whitespace-pre-wrap">{event.description}</p>
                </div>
            )}

            {/* Financial Summary */}
            <div className="card bg-gray-50">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Resumen Financiero</h2>
                <div className="space-y-2">
                    <div className="flex justify-between">
                        <span className="text-gray-600">Total Ingresos:</span>
                        <span className="font-bold text-gray-900">{formatCurrency(event.total_revenue || 0)}</span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-gray-600">Costo Total:</span>
                        <span className="font-bold text-gray-900">{formatCurrency(event.total_cost || 0)}</span>
                    </div>
                    <div className="flex justify-between pt-2 border-t border-gray-200">
                        <span className="text-gray-900 font-medium">Ganancia:</span>
                        <span className="font-bold text-green-600">
                            {formatCurrency((event.total_revenue || 0) - (event.total_cost || 0))}
                        </span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-gray-900 font-medium">Margen:</span>
                        <span className="font-bold text-blue-600">
                            {((event.margin || 0) * 100).toFixed(1)}%
                        </span>
                    </div>
                </div>
            </div>
        </div>
    );
}
