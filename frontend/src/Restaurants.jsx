import { useState, useEffect } from 'react';
import axios from 'axios';

function Restaurants() {
    const [searchTerm, setSearchTerm] = useState('');
    const [restaurants, setRestaurants] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchRestaurants() {
            try {
                setIsLoading(true);

                const response = await axios.get('/api/restaurants', {
                    params: {
                        q: searchTerm
                    }
                });

                const isOk = response.status >= 200 && response.status < 300
                if (!isOk) {
                    // `error` field defined by the backend
                    setError(response.error);
                    return;
                }

                const { data } = response.data;
                setRestaurants(data);
            } catch (error) {
                setError(error.message);
            } finally {
                setIsLoading(false);
            }
        }

        fetchRestaurants();
    }, [searchTerm]);

    return (
        <div>
            <form className="max-w-md mx-auto">
                <div class="relative">
                    <div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
                        <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
                        </svg>
                    </div>
                    <input
                        type="search"
                        class="block w-full p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        placeholder="Search Restaurants..."
                        value={searchTerm}
                        onChange={e => setSearchTerm(e.target.value)}
                    />
                </div>
            </form>

            {isLoading && <p>Loading...</p>}
            {error && <p className="text-red-800">{error}</p>}

            <div class="relative overflow-x-auto">

                <table className="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                        <tr>
                            <th scope="col" className="px-6 py-3">Name</th>
                            <th scope="col" className="px-6 py-3">Phone</th>
                            <th scope="col" className="px-6 py-3">Address</th>
                        </tr>
                    </thead>
                    <tbody>
                        {restaurants.map(restaurant => (
                            <tr
                                key={restaurant.restaurant_id || index}
                                className="bg-white border-b dark:bg-gray-800 dark:border-gray-700 border-gray-200"
                            >
                                <th
                                    scope="row"
                                    className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                                >
                                    {restaurant.name}
                                </th>
                                <td className="px-6 py-4">{restaurant.phone}</td>
                                <td className="px-6 py-4">{`${restaurant.address}, ${restaurant.city}, ${restaurant.state} ${restaurant.zip_code}`}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default Restaurants;