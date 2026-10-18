import sys
import unittest

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from start import load_data, normalize_vietnamese, filter_reports


class TestFilterAndSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Tải dữ liệu mẫu từ data.json trước khi chạy test."""
        cls.data = load_data()
        cls.reports = cls.data.get('reports', [])
        cls.groups = cls.data.get('groups', [])

    def test_01_total_reports_count(self):
        """Kiểm tra tổng số lượng báo cáo mẫu ban đầu (phải đủ 12 báo cáo)."""
        self.assertEqual(len(self.reports), 12, "Dữ liệu mẫu ban đầu phải có đúng 12 báo cáo.")

    def test_02_normalize_vietnamese(self):
        """Kiểm tra hàm chuẩn hóa tiếng Việt: bỏ dấu, xử lý chữ đ/Đ, chuyển chữ thường (FR-06)."""
        self.assertEqual(normalize_vietnamese("GIÁM SÁT"), "giam sat")
        self.assertEqual(normalize_vietnamese("Tiến độ nhập học"), "tien do nhap hoc")
        self.assertEqual(normalize_vietnamese("Đường dẫn ĐẦU TIÊN"), "duong dan dau tien")

    def test_03_search_exact_and_unaccented(self):
        """
        Kiểm tra tìm kiếm không phân biệt hoa thường và dấu tiếng Việt (FR-06):
        - Tìm 'giam sat' phải ra đúng 3 báo cáo (R02, R05, R10).
        """
        results = filter_reports(self.reports, query="giam sat")
        self.assertEqual(len(results), 3, "Tìm 'giam sat' phải ra đúng 3 báo cáo.")
        ids = [r['id'] for r in results]
        self.assertIn('R02', ids)
        self.assertIn('R05', ids)
        self.assertIn('R10', ids)

    def test_04_search_keyword_doanh_thu(self):
        """
        Tiêu chí chấp nhận FR-06:
        - Tìm 'doanh thu' phải ra đúng 2 báo cáo (R06, R09).
        """
        results = filter_reports(self.reports, query="doanh thu")
        self.assertEqual(len(results), 2, "Tìm 'doanh thu' phải ra đúng 2 báo cáo.")
        ids = [r['id'] for r in results]
        self.assertIn('R06', ids)
        self.assertIn('R09', ids)

    def test_05_filter_by_group(self):
        """
        Tiêu chí chấp nhận FR-03:
        - Chọn nhóm SKR phải còn đúng 4 báo cáo (R04, R05, R06, R07).
        - Bỏ lọc (None) phải trả về đủ 12 báo cáo.
        """
        skr_reports = filter_reports(self.reports, group="SKR")
        self.assertEqual(len(skr_reports), 4, "Lọc nhóm SKR phải ra đúng 4 báo cáo.")

        all_reports = filter_reports(self.reports, group=None)
        self.assertEqual(len(all_reports), 12, "Bỏ lọc phải trả về đủ 12 báo cáo.")

    def test_06_combined_filter_and_search(self):
        """
        Tiêu chí chấp nhận FR-06:
        - Chọn nhóm SKR rồi tìm 'giam sat' phải ra đúng 1 báo cáo (R05: Giám sát tiến độ nhập học).
        """
        results = filter_reports(self.reports, group="SKR", query="giam sat")
        self.assertEqual(len(results), 1, "Chọn SKR và tìm 'giam sat' phải ra đúng 1 báo cáo.")
        self.assertEqual(results[0]['id'], 'R05')


if __name__ == '__main__':
    print("=" * 60)
    print("CHẠY BỘ KIỂM THỬ TỰ ĐỘNG (DOC-04): LỌC & TÌM KIẾM BÁO CÁO")
    print("=" * 60)
    unittest.main(verbosity=2)
