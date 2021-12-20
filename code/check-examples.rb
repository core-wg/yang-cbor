require 'rexml/document'

ENV["UPPERCASE_HEX"] = "true"

require 'cbor-pure'
require 'cbor-pretty'
require 'treetop'
require 'cbor-diag-parser'
parser = CBOR_DIAGParser.new

doc = REXML::Document.new(File.read("draft-ietf-core-yang-cbor.xml"))

cnt = Hash.new(0)
pretty = nil
REXML::XPath.each(doc.root, "//sourcecode") { |e|
  t = e.attributes["type"]
  cnt[t] += 1
  case t
  when "yang"
  when "cbor-diag"
    data = parser.parse(e.text).to_rb
    pretty = CBOR::pretty(CBOR::encode(data))
  when "cbor-pretty"
    if pretty && pretty != e.text
      puts
      File.write(".c.gen", pretty)
      File.write(".c.doc", e.text)
      puts `git diff -U1 --word-diff --no-index --  .c.gen .c.doc`
      puts "=" * 72
    end
    pretty = nil
  else
    warn "*** Unknown sourcecode type #{t}"
  end
}
p cnt
