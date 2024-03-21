
import pandas as pd
import centerline_width as cw
df = pd.read_csv("/Users/raisa/Work/QGISPlugins/hapt-qgis-plugin/notebook/sampled_points.csv")
ro = cw.riverCenterline(df)
print(cw.getCenterlineAsGeometry(ro).wkt)
