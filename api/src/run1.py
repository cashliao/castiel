# -*- coding: utf-8 -*-
import formosa as fa
import pandas as pd

fa.download_new_csv()
fa.download_old_csv()
new_members = fa.resolve_new_members(fa.load_new_csv())
old_members = fa.resolve_old_members(fa.load_old_csv())
all_members = fa.get_all_members(new_members,old_members)
summary_report = fa.get_summary_report(all_members)
# print(summary_report)
