@u = %{[^"\n]*}; @q = @u + '"'
puts ARGF.read.gsub(/^(#@q(#@q#@q)*#@u) *\n +(#@q)/, "\\1\\3")
