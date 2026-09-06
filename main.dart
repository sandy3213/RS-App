import 'package:flutter/material.dart';

void main() {
  runApp(const RSSecuritiesApp());
}

class RSSecuritiesApp extends StatelessWidget {
  const RSSecuritiesApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'RS Securities',
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF0F172A),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF10B981),
        ),
      ),
      home: const DashboardScreen(),
    );
  }
}

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('RS Securities Pvt Ltd'),
        backgroundColor: const Color(0xFF1E293B),
        elevation: 0,
        actions: [
          IconButton(icon: const Icon(Icons.notifications_none), onPressed: () {}),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: const Color(0xFF1E293B),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: Colors.white10),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Total Portfolio Value', style: TextStyle(color: Colors.grey, fontSize: 14)),
                  const SizedBox(height: 8),
                  const Text('₹ 2,45,890.50', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.white)),
                  const SizedBox(height: 12),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: const [
                      Text('1-Day Returns', style: TextStyle(color: Colors.grey)),
                      Text('+₹ 4,230.00 (1.75%)', style: TextStyle(color: Color(0xFF10B981), fontWeight: FontWeight.bold)),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),
            const Text('Market Watchlist', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
            const SizedBox(height: 12),
            _buildStockTile('NIFTY 50', '22,450.30', '+112.40 (+0.50%)', true),
            _buildStockTile('BANK NIFTY', '47,820.10', '-85.20 (-0.18%)', false),
            _buildStockTile('RELIANCE', '2,980.00', '+34.50 (+1.17%)', true),
            _buildStockTile('TCS', '3,850.75', '-12.30 (-0.32%)', false),
          ],
        ),
      ),
    );
  }

  static Widget _buildStockTile(String name, String price, String change, bool isPositive) {
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF1E293B),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Colors.white)),
          Column(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Text('₹ $price', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Colors.white)),
              Text(change, style: TextStyle(color: isPositive ? const Color(0xFF10B981) : Colors.red, fontSize: 12)),
            ],
          ),
        ],
      ),
    );
  }
}
